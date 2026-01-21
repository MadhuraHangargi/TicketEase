SHOW DATABASES;
SHOW TABLES;
SELECT count(*) FROM tickets_file_t; 
CREATE INDEX ts ON tickets_file_t (created_at);
CREATE INDEX ts ON tickets_file_t (resolved_at);