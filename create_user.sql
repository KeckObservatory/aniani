-- Create a new user
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'test';

-- Grant privileges to the new user on a specific database
GRANT ALL PRIVILEGES ON aniani.* TO 'test'@'localhost';

-- Or grant all privileges on all databases
-- GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;

