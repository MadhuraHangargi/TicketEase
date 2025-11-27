TicketEase – IT Ticketing System 
Project Overview:
TicketEase is a full-stack IT Ticket Management System designed to streamline issue reporting, SLA monitoring, file uploads, role-based workflows, and analytics dashboards. It is built using Flask, MySQL, Bootstrap 5, and Power BI.

Key Features:
• Create IT support tickets
• Automatic priority classification (keyword-based + VIP boost)
• Ticket categories: Access, Email, Network, Printer, Database, Other IT
• Ticket lifecycle: Open → In Progress → Resolved → Closed
• File uploads (images, PDFs, logs, ZIP)
• Role-based workflows (Employee, Support Agent, Admin)
• Web dashboards using Chart.js
• Admin analytics in Power BI (SLA, backlog trends, workloads)

Tech Stack:
Backend: Python, Flask, MySQL
Frontend: HTML, CSS, Bootstrap 5, JavaScript, Chart.js
Other: Power BI, DataTables, File Upload Handling




Folder Structure:
ticket_app_enterprise/
│── app.py
│── requirements.txt
│── uploads/
│── templates/
│     ├── base.html
│     ├── home.html
│     ├── new_ticket.html
│     ├── tickets.html
│     └── ticket_detail.html
│── static/
└── README.md

Database Schema
TICKETS TABLE:
ticket_id (PK)
issue
employee_name
issue_category
dept_id
target_resolution_hours
created_at
resolved_at
user_id


ATTACHMENTS TABLE:
attachment_id (PK)
ticket_id (FK)
file_name
file_path
uploaded_by
uploaded_at


Installation Guide
1. Clone repository:
git clone https://github.com/<your-username>/TicketEase.git
2. Create virtual environment:
python -m venv venv
3. Activate:
venv\Scripts\activate (Windows)
4. Install dependencies:
pip install -r requirements.txt
5. Create MySQL database:
CREATE DATABASE ticketing_db;
6. Create MySQL user:
CREATE USER 'ticketuser'@'localhost' IDENTIFIED BY 'yourpassword';
7. Grant privileges:
GRANT ALL PRIVILEGES ON ticketing_db.* TO 'ticketuser'@'localhost';
8. Run Flask:
python app.py
9. Access application:
http://127.0.0.1:5000s



Author:
Madhura Hangargi
B.Tech CSE (AI/ML)
Email: madhurahangargi@gmail.com
LinkedIn: linkedin.com/in/madhura-hangargi
