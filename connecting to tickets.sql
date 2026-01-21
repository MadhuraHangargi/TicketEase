UPDATE tickets t
JOIN users u ON t.employee_name = u.name
SET t.user_id = u.user_id
WHERE 1=1;
SHOW COLUMNS FROM tickets LIKE 'user_id';

SET SQL_SAFE_UPDATES = 0;
SELECT @@sql_safe_updates;  -- should return 0

UPDATE tickets t
JOIN departments d ON t.issue_category = d.dept_name
SET t.dept_id = d.dept_id
WHERE 1=1;

SELECT * FROM users ;
SELECT * FROM departments LIMIT 5;


ALTER TABLE tickets
ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id),
ADD CONSTRAINT fk_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id);

SELECT t.ticket_id, u.name AS employee, d.dept_name AS department, t.status
FROM tickets t
JOIN users u ON t.user_id = u.user_id
JOIN departments d ON t.dept_id = d.dept_id
LIMIT 10;


