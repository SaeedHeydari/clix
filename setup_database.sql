-- Create database for the MyCLI project
CREATE DATABASE IF NOT EXISTS mycli_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Grant privileges (optional - if you want to create a specific user)
-- CREATE USER IF NOT EXISTS 'mycli_user'@'localhost' IDENTIFIED BY 'your_password';
-- GRANT ALL PRIVILEGES ON mycli_db.* TO 'mycli_user'@'localhost';
-- FLUSH PRIVILEGES;

USE mycli_db;