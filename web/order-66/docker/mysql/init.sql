-- MySQL Initialization Script for Order 66 CTF Challenge
-- This script runs automatically when the MySQL container starts for the first time

-- Set timezone
SET time_zone = '+00:00';

-- Configure MySQL for better CTF experience
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';

-- Create additional CTF user with broader permissions for easier database exploration
-- This makes it easier for CTF participants to explore the database
GRANT ALL PRIVILEGES ON *.* TO 'vader'@'%' WITH GRANT OPTION;
CREATE USER IF NOT EXISTS 'empire_user'@'%' IDENTIFIED BY 'darkside';
GRANT SELECT, INSERT, UPDATE, DELETE ON `empire_todos`.* TO 'empire_user'@'%';

-- Create a read-only user for reconnaissance
CREATE USER IF NOT EXISTS 'rebel_spy'@'%' IDENTIFIED BY 'hope';
GRANT SELECT ON `empire_todos`.* TO 'rebel_spy'@'%';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;

-- Use the application database
USE empire_todos;

-- Create a view that might help CTF participants
CREATE OR REPLACE VIEW empire_intelligence AS
SELECT 'The Empire has hidden secrets in the database' as hint,
       'Try exploring different tables and columns' as tip,
       'The sorting functionality might be vulnerable' as vulnerability_hint;

-- Add some metadata
CREATE TABLE IF NOT EXISTS ctf_metadata (
    id INT PRIMARY KEY AUTO_INCREMENT,
    challenge_name VARCHAR(255) DEFAULT 'Order 66: Execute the Query',
    difficulty VARCHAR(50) DEFAULT 'Intermediate',
    category VARCHAR(50) DEFAULT 'SQL Injection',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO ctf_metadata (challenge_name, difficulty, category) 
VALUES ('Order 66: Execute the Query', 'Intermediate', 'SQL Injection')
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- Success message
SELECT '🏴 Order 66 MySQL Database initialized successfully!' as message;