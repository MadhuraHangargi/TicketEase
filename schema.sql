CREATE DATABASE IF NOT EXISTS ticketing_db;
USE ticketing_db;

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    issue VARCHAR(250),
    employee_name VARCHAR(100),
    issue_category VARCHAR(50),
    priority VARCHAR(20),
    target_resolution_hours INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    status ENUM('Open','In Progress','Resolved','Closed') DEFAULT 'Open'
);

CREATE TABLE IF NOT EXISTS attachments (
    attachment_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_by VARCHAR(100),
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
);

INSERT INTO tickets (issue, employee_name, issue_category, priority, target_resolution_hours, status, resolved_at) VALUES
('Laptop not starting', 'Madhura', 'Hardware', 'High', 24, 'Open', NULL),
('Password reset required', 'Diya', 'Access', 'Low', 12, 'Resolved', NOW()),
('VPN connection failing', 'Ravi', 'Network', 'Critical', 8, 'In Progress', NULL),
('Email not syncing', 'Anita', 'Email', 'Medium', 24, 'Closed', NOW()),
('Database timeout error', 'Vikram', 'Database', 'Critical', 48, 'Resolved', NOW());

INSERT INTO attachments (ticket_id, file_name, file_path, uploaded_by) VALUES
(1, 'error_log.txt', 'dummy_error_log.txt', 'Madhura'),
(3, 'vpn_issue.png', 'dummy_vpn_issue.png', 'Ravi'),
(5, 'db_screenshot.jpg', 'dummy_db_screenshot.jpg', 'Vikram');
