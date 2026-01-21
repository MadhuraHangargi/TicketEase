TICKETEASE- A full-stack IT Ticketing & Support Management System built to handle employee IT issues, automate ticket priority, track SLAs, and analyze support performance using dashboards.

📌 Project Overview

This project simulates an enterprise IT support workflow where employees raise IT issues and support teams manage them efficiently.

The system focuses on:
	•	Ticket lifecycle management
	•	Automated priority assignment
	•	SLA tracking
	•	File attachments
	•	Data analytics and reporting

It demonstrates database design, backend development, ETL-style data handling, and analytics integration.

#Ticket Lifecycle
	•	Open → In Progress → Resolved → Closed
	•	Resolution timestamps stored automat

#Automated Priority Assignment
	•	Keyword-based classification
	•	Priority levels:
	•	Low
	•	Medium
	•	High
	•	Critical
	•	VIP/Admin users receive priority escalation

#Dashboards & Analytics
	•	Tickets by priority
	•	Tickets by status
	•	SLA compliance analysis
	•	Backlog and workload trends

  
#FOLDER STRUCTURE:
TicketEase/
│── app.py
│── README.md
│── requirements.txt
│
├── sql/
│   ├── schema.sql
│   ├── usersFINAL.sql
│   ├── DEPARTMENTSFINAL.sql
│   ├── final table.sql
│   ├── FINALCOMMENTS.sql
│   ├── ticketing_dwh.sql
│
├── data/
│   ├── tickets_dataset_final.csv
│   ├── comments_dataset.csv
│   ├── users_dataset_staging.csv
│   ├── dim_date.csv
│
├── templates/
    ├── base.html
    ├── home.html
    ├── new_ticket.html
    ├── tickets.html
    └── ticket_detail.html

├── static/
│   ├── logo.png
│   └── bg.jpg
