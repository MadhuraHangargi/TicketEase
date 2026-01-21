#ROW COUNT FOR THE REGULAR ANALYSIS
select count(*) FROM tickets;

#CHECK THE TICKETS PER STATUS
select status, COUNT(*)
FROM tickets 
GROUP BY status;

#TICKETS PER CATEGORY
select issue_category, COUNT(*)
FROM tickets
GROUP BY issue_category;

#AVG RESOLUTION HOURS 
SELECT AVG(target_resolution_hours) AS avg_resolution_hours
FROM tickets;

#EARLIEST/LATEST DATES
SELECT MIN(created_at) AS first_ticket, MAX(created_at) AS last_ticket
FROM tickets;