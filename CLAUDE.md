# CLAUDE.md - Project Overview for AI Assistance

## Project Name
ToroBX CLI (Python CLI with MySQL Database and Migrations)

## Repository
- **URL**: https://github.com/SaeedHeydari/clix.git
- **Main Branch**: main

## Purpose
A Python CLI application for adding data form sources in @data directory with MySQL database backend.

## Tech Stack
- **Language**: Python 3
- **CLI Framework**: Click 8.1.7
- **ORM**: SQLAlchemy 2.0.23
- **Database**: MySQL (via PyMySQL 1.1.0)
- **Migrations**: Alembic 1.13.1
- **Configuration**: python-dotenv 1.0.0

## Project Structure
```
torobx/
├── cli.py                 # Main CLI application entry point
├── mycli/                 # Core application package
│   ├── __init__.py
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection setup
│   └── models.py         # SQLAlchemy models (User, Category, Brand)
├── migrations/           # Alembic migration files
│   ├── env.py
│   ├── script.py.mako
│   └── versions/         # Migration version files
├── data/                 # Data files for import
├── tests/                # Test directory
├── setup_mysql.sh        # MySQL setup script
├── setup_database.sql    # Database setup SQL
├── alembic.ini          # Alembic configuration
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Database Models

### Category Model
- **Table**: categories
- **Fields**: id, title, english_title, description, image, icon, category_parent_id, brand, order, visible, is_active, filterable_by_brand, background_color, absolute_url, created_at, updated_at
- **Features**: Hierarchical category structure with parent-child relationships

### Brand Model
- **Table**: brands
- **Fields**: id, slug, name1 (Persian), name2 (English), created_at, updated_at
- **Features**: Brand management with multilingual support

## Available CLI Commands

### Database Management
- `python cli.py init-db` - Initialize database tables
- `python cli.py drop-db` - Drop all database tables (with confirmation)
- `python cli.py migrate "<message>"` - Create a new migration
- `python cli.py upgrade` - Apply pending migrations
- `python cli.py downgrade` - Rollback one migration

### Category Management
- `python cli.py import-categories <json_file>` - Import categories from JSON
- `python cli.py list-categories` - List all categories
- `python cli.py tree-categories` - Display categories in tree structure
  - `--parent-id` - Show only children of specific parent
  - `--active-only` - Show only active categories


## Key Features
1. **Database Migrations**: Full migration support with Alembic for schema versioning
3. **Data Import**: JSON import functionality for bulk data operations
4. **Interactive CLI**: User-friendly command-line interface with prompts and confirmations
