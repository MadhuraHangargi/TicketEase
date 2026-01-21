CREATE TABLE tickets ( 
Ticket_id INT AUTO_INCREMENT PRIMARY KEY, 
Issue VARCHAR (250), 
Employee_name VARCHAR(100), 
Issue_category VARCHAR(50), 
Priority VARCHAR(20), 
Target_resolution_hours INT, 
Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
Resolved_at TIMESTAMP, 
Status VARCHAR (20) CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Closed')) 
);
SHOW TABLES;
DESCRIBE tickets;

