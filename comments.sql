CREATE TABLE tickets(
ticket_id INT AUTO_INCREMENT PRIMARY KEY,
issue VARCHAR(250),
employee_name VARCHAR(100),
issue_category VARCHAR(50),
priority VARCHAR(20),
target_resolution_hours INT,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
resolved_at DATETIME,
status ENUM ('Open',' In Progress', 'Resolved', 'Closed')
);
