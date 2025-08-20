#!/usr/bin/env python3
import click
from sqlalchemy.orm import Session
from mycli.database import SessionLocal, engine
from mycli.models import User, Base
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
@click.option('--username', prompt=True, help='Username for the new user')
@click.option('--email', prompt=True, help='Email for the new user')
@click.option('--full-name', prompt=True, help='Full name for the new user')
def create_user(username, email, full_name):
    """Create a new user"""
    db = SessionLocal()
    try:
        user = User(username=username, email=email, full_name=full_name)
        db.add(user)
        db.commit()
        click.echo(f"User '{username}' created successfully!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error creating user: {e}")
    finally:
        db.close()

@cli.command()
def list_users():
    """List all users"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        if not users:
            click.echo("No users found.")
            return
        
        click.echo("\nUsers:")
        click.echo("-" * 80)
        for user in users:
            click.echo(f"ID: {user.id} | Username: {user.username} | Email: {user.email} | Active: {user.is_active}")
    finally:
        db.close()

@cli.command()
@click.argument('username')
def delete_user(username):
    """Delete a user by username"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            click.echo(f"User '{username}' not found.")
            return
        
        if click.confirm(f"Are you sure you want to delete user '{username}'?"):
            db.delete(user)
            db.commit()
            click.echo(f"User '{username}' deleted successfully!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error deleting user: {e}")
    finally:
        db.close()

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

if __name__ == '__main__':
    cli()