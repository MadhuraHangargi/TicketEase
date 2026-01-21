CREATE TABLE users(
user_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL, 
email VARCHAR(100) UNIQUE NOT NULL, 
role VARCHAR(50) NOT NULL
);

INSERT INTO users (name, email,role)
SELECT DISTINCT
employee_name,
'temp@example.com' AS email, 
'support_agent' AS role
FROM tickets;
