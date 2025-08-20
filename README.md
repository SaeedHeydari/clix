# Python CLI with MySQL Database and Migrations

A Python CLI application using Click framework with SQLAlchemy ORM and Alembic for database migrations.

## Features

- Command-line interface built with Click
- MySQL database connection using SQLAlchemy
- Database migrations with Alembic
- Sample User model with CRUD operations

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database:
   - Copy `.env.example` to `.env`
   - Update the `DATABASE_URL` with your MySQL credentials:
     ```
     DATABASE_URL=mysql+pymysql://username:password@localhost:3306/dbname
     ```

4. Create the database in MySQL:
```sql
CREATE DATABASE dbname;
```

## Usage

### Database Commands

Initialize database tables:
```bash
python cli.py init-db
```

Create and apply migrations:
```bash
# Create a new migration
python cli.py migrate "Add users table"

# Apply migrations
python cli.py upgrade

# Rollback one migration
python cli.py downgrade
```

### User Management Commands

Create a new user:
```bash
python cli.py create-user
```

List all users:
```bash
python cli.py list-users
```

Delete a user:
```bash
python cli.py delete-user <username>
```

### Drop all tables (careful!):
```bash
python cli.py drop-db
```

## Project Structure

```
.
├── mycli/
│   ├── __init__.py
│   ├── config.py       # Configuration settings
│   ├── database.py     # Database connection setup
│   └── models.py       # SQLAlchemy models
├── migrations/
│   ├── env.py          # Alembic environment
│   ├── script.py.mako  # Migration template
│   └── versions/       # Migration files
├── tests/              # Test directory
├── .env.example        # Example environment file
├── alembic.ini         # Alembic configuration
├── cli.py              # Main CLI application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Sample Model

The project includes a `User` model with the following fields:
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `full_name`: User's full name
- `is_active`: Boolean flag for active users
- `created_at`: Timestamp when created
- `updated_at`: Timestamp when last updated