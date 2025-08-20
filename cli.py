#!/usr/bin/env python3
import click
import json
from sqlalchemy.orm import Session
from mycli.database import SessionLocal, engine
from mycli.models import User, Category, Brand, Base
import alembic.config

@click.group()
def cli():
    """MyCLI - A Python CLI with MySQL database and migrations"""
    pass

@cli.command()
def init_db():
    """Initialize the database with all tables"""
    Base.metadata.create_all(bind=engine)
    click.echo("Database initialized successfully!")

@cli.command()
def drop_db():
    """Drop all database tables"""
    if click.confirm("Are you sure you want to drop all tables?"):
        Base.metadata.drop_all(bind=engine)
        click.echo("All tables dropped!")

@cli.command()
@click.argument('message')
def migrate(message):
    """Create a new migration"""
    alembic_args = [
        '--raiseerr',
        'revision',
        '--autogenerate',
        '-m', message
    ]
    alembic.config.main(argv=alembic_args)
    click.echo(f"Migration '{message}' created successfully!")

@cli.command()
def upgrade():
    """Apply all pending migrations"""
    alembic_args = [
        '--raiseerr',
        'upgrade', 'head'
    ]
    alembic.config.main(argv=alembic_args)
    click.echo("Database upgraded successfully!")

@cli.command()
def downgrade():
    """Downgrade database by one migration"""
    alembic_args = [
        '--raiseerr',
        'downgrade', '-1'
    ]
    alembic.config.main(argv=alembic_args)
    click.echo("Database downgraded successfully!")

@cli.command()
@click.argument('json_file', type=click.Path(exists=True))
def import_categories(json_file):
    """Import categories from JSON file"""
    db = SessionLocal()
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        categories = data.get('results', [])
        imported = 0

        # First pass: Create all categories without parent relationships
        for cat_data in categories:
            existing = db.query(Category).filter(Category.id == cat_data['id']).first()
            if not existing:
                category = Category(
                    id=cat_data['id'],
                    title=cat_data['title'],
                    english_title=cat_data.get('english_title'),
                    description=cat_data.get('description'),
                    image=cat_data.get('image'),
                    icon=cat_data.get('icon'),
                    brand=cat_data.get('brand'),
                    order=cat_data.get('order', 0),
                    visible=cat_data.get('visible', True),
                    is_active=cat_data.get('is_active', True),
                    filterable_by_brand=cat_data.get('filterable_by_brand', False),
                    background_color=cat_data.get('background_color'),
                    absolute_url=cat_data.get('absolute_url')
                )
                db.add(category)
                imported += 1

        db.commit()

        # Second pass: Update parent relationships
        for cat_data in categories:
            if cat_data.get('category_parent'):
                category = db.query(Category).filter(Category.id == cat_data['id']).first()
                if category:
                    category.category_parent_id = cat_data['category_parent']

        db.commit()
        click.echo(f"Imported {imported} categories successfully!")

    except Exception as e:
        db.rollback()
        click.echo(f"Error importing categories: {e}")
    finally:
        db.close()

@cli.command()
def list_categories():
    """List all categories"""
    db = SessionLocal()
    try:
        categories = db.query(Category).order_by(Category.order, Category.id).all()
        if not categories:
            click.echo("No categories found.")
            return

        click.echo("\nCategories:")
        click.echo("-" * 100)
        for cat in categories:
            parent_name = cat.parent.title if cat.parent else "None"
            click.echo(f"ID: {cat.id} | Title: {cat.title} | English: {cat.english_title} | Parent: {parent_name} | Active: {cat.is_active}")
    finally:
        db.close()

@cli.command()
@click.option('--parent-id', type=int, help='Show only children of specific parent category')
@click.option('--active-only', is_flag=True, help='Show only active categories')
def tree_categories(parent_id, active_only):
    """Display categories in tree structure"""
    db = SessionLocal()
    try:
        def print_tree(category, level=0):
            if active_only and not category.is_active:
                return
            indent = "  " * level + "└─ " if level > 0 else ""
            click.echo(f"{indent}{category.title} (ID: {category.id})")
            for child in sorted(category.children, key=lambda x: (x.order, x.id)):
                print_tree(child, level + 1)

        if parent_id:
            root_cats = db.query(Category).filter(Category.id == parent_id).all()
        else:
            root_cats = db.query(Category).filter(Category.category_parent_id == None).order_by(Category.order, Category.id).all()

        for cat in root_cats:
            print_tree(cat)
    finally:
        db.close()

@cli.command()
@click.argument('json_file', type=click.Path(exists=True))
@click.option('--category-id', type=int, help='Category ID to associate brands with')
def import_brands(json_file, category_id):
    """Import brands from JSON file and optionally associate with a category"""
    db = SessionLocal()
    try:
        # Check if category exists when category_id is provided
        if category_id:
            category = db.query(Category).filter(Category.id == category_id).first()
            if not category:
                click.echo(f"Category with ID {category_id} not found.")
                return

        with open(json_file, 'r', encoding='utf-8') as f:
            brands_data = json.load(f)

        imported = 0
        updated = 0

        for brand_data in brands_data:
            # Skip the "not detected" brand with id -1
            if brand_data['id'] == -1:
                continue

            existing = db.query(Brand).filter(Brand.id == brand_data['id']).first()
            if existing:
                # Update existing brand
                existing.slug = brand_data['slug']
                existing.name1 = brand_data['name1']
                existing.name2 = brand_data['name2']
                if category_id:
                    existing.category_id = category_id
                updated += 1
            else:
                # Create new brand
                brand = Brand(
                    id=brand_data['id'],
                    slug=brand_data['slug'],
                    name1=brand_data['name1'],
                    name2=brand_data['name2'],
                    category_id=category_id if category_id else None
                )
                db.add(brand)
                imported += 1

        db.commit()
        if category_id:
            click.echo(f"Imported {imported} new brands and updated {updated} existing brands, associated with category ID {category_id}!")
        else:
            click.echo(f"Imported {imported} new brands and updated {updated} existing brands successfully!")

    except Exception as e:
        db.rollback()
        click.echo(f"Error importing brands: {e}")
    finally:
        db.close()

@cli.command()
@click.option('--category-id', type=int, help='Filter brands by category ID')
def list_brands(category_id):
    """List all brands, optionally filtered by category"""
    db = SessionLocal()
    try:
        query = db.query(Brand)
        if category_id:
            query = query.filter(Brand.category_id == category_id)

        brands = query.order_by(Brand.name2).all()
        if not brands:
            if category_id:
                click.echo(f"No brands found for category ID {category_id}.")
            else:
                click.echo("No brands found.")
            return

        click.echo("\nBrands:")
        click.echo("-" * 100)
        for brand in brands:
            cat_info = f" | Category: {brand.category.title if brand.category else 'None'}"
            click.echo(f"ID: {brand.id} | English: {brand.name2} | Persian: {brand.name1}{cat_info}")
    finally:
        db.close()


if __name__ == '__main__':
    cli()
