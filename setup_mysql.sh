#!/bin/bash

echo "MySQL Database Setup for MyCLI Project"
echo "======================================"
echo ""
echo "This script will help you create the database."
echo ""

# Check which MySQL to use
if [ -f "/opt/lampp/bin/mysql" ]; then
    MYSQL_CMD="/opt/lampp/bin/mysql"
    echo "Using XAMPP MySQL at: $MYSQL_CMD"
else
    MYSQL_CMD="mysql"
    echo "Using system MySQL"
fi

echo ""
echo "Please make sure MySQL is running before continuing."
echo "For XAMPP: sudo /opt/lampp/lampp start"
echo "For system MySQL: sudo systemctl start mysql"
echo ""
read -p "Press Enter when MySQL is running..."

echo ""
echo "Creating database..."
$MYSQL_CMD -u root < setup_database.sql

if [ $? -eq 0 ]; then
    echo "✓ Database 'mycli_db' created successfully!"
else
    echo "✗ Failed to create database. Please check:"
    echo "  1. MySQL is running"
    echo "  2. You have the correct permissions"
    echo "  3. The root user doesn't require a password (or add -p flag)"
    exit 1
fi

echo ""
echo "Database setup complete!"
echo "You can now run migrations with: python cli.py upgrade"