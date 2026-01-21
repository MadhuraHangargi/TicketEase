INSERT INTO tickets (
ticket_id,
issue,
employee_name,
issue_category,
priority,
target_resolution_hours,
created_at,
resolved_at,
status
)
SELECT 
CAST(TRIM(ticket_id) AS UNSIGNED),
TRIM(issue),
TRIM(employee_name),
TRIM(issue_category),
TRIM(priority),
CAST(TRIM(target_resolution_hours) AS UNSIGNED),
STR_TO_DATE(TRIM(created_at), '%d-%m-%Y %H:%i'),
CASE 
WHEN TRIM(resolved_at) = '' THEN NULL
ELSE STR_TO_DATE(TRIM(resolved_at), '%d-%m-%Y %H:%i')
END,
CASE TRIM(status)
WHEN 'Open' THEN 'Open'
WHEN 'In Progress' THEN 'In Progress'
WHEN 'Resolved' THEN 'Resolved'
WHEN 'Closed' THEN 'Closed'
ELSE NULL
END 
FROM tickets_staging;