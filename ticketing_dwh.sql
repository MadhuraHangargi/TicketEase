USE ticketing_dwh;

CREATE TABLE dim_user (
user_key INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR (100),
email VARCHAR(100),
role VARCHAR(50)
);

INSERT INTO dim_user (name, email, role)
SELECT DISTINCT name, email, role
FROM ticketing_db.users;

SELECT * FROM dim_user;


CREATE TABLE dim_priority (
priority_key INT AUTO_INCREMENT PRIMARY KEY,
priority_name VARCHAR(20)
); 

INSERT INTO dim_priority(priority_name)
VALUES 
('Low'),
('Medium'),
('High'),
('Critical');
SELECT * FROM dim_priority;



CREATE TABLE dim_date (
date_key INT PRIMARY KEY,
date_value DATE,
year INT,
day INT,
quanter INT,
week_of_year INT,
day_of_year int
);
SELECT COUNT(*) FROM dim_date;   -- should be ~730 rows
SELECT * FROM dim_date LIMIT 5;


CREATE TABLE Fact_tickets (
fact_id INT AUTO_INCREMENT PRIMARY KEY,
ticket_id INT,
user_key INT,
dept_key INT,
priority_key INT,
Status_key INT,
created_date_key INT,
resolved_date_key INT,
target_resolution_hours INT,
actual_resolution_hours INT,
sla_met_flag TINYINT,
created_at DATETIME,
resolved_at DATETIME
);

CREATE TABLE dim_status (
    status_key INT AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(20)
);

INSERT INTO dim_status (status_name)
VALUES 
('Open'),
('In Progress'),
('Resolved'),
('Closed');
SELECT * FROM dim_status;

CREATE TABLE dim_department (
    dept_key INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100)
);

INSERT INTO dim_department (dept_name)
SELECT DISTINCT dept_name
FROM ticketing_db.departments; # ticketing.db the databaase name nd then .departments means the table inside the database which we want

SELECT * FROM dim_department;


SHOW TABLES;
DESCRIBE fact_tickets;
DESCRIBE dim_user;