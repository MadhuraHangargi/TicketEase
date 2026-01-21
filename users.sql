CREATE TABLE users (
user_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
role ENUM('customer', 'support_agent', 'admin') NOT NULL
);
