CREATE TABLE tickets ( 
    ticket_id SERIAL PRIMARY KEY, 
    issue VARCHAR (250),
    employee_name VARCHAR(100),
    issue_category VARCHAR(50),
    priority VARCHAR(20),
    target_resolution_hours INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    status VARCHAR (20) CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Closed'))
);