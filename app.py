from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
import mysql.connector, os, time, json, traceback
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- Debug routes (only defined once) ---
@app.route('/ping')
def ping():
    return 'pong', 200

@app.route('/tickets_debug')
def tickets_debug():
    try:
        conn = get_db_connection()
        if not conn:
            return "<h3>DB connection failed (get_db_connection returned None)</h3>", 500

        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT ticket_id, issue, employee_name, status, created_at FROM tickets ORDER BY ticket_id DESC LIMIT 5")
        rows = cur.fetchall()
        cur.close(); conn.close()
        return "<h3>Fetched {} rows</h3><pre>{}</pre>".format(len(rows), json.dumps(rows, default=str, indent=2))
    except Exception:
        tb = traceback.format_exc()
        print("DEBUG ERROR:", tb)
        return "<h3>Exception occurred</h3><pre>{}</pre>".format(tb.replace("<","&lt;").replace(">","&gt;")), 500

# --- config ---
app.secret_key = 'change-this-secret'
BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXT = {'png','jpg','jpeg','gif','pdf','txt','log','zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db_config = {
    'host': 'localhost',
    'user': 'ticketuser',
    'password': 'Diya1madhura*',
    'database': 'ticketing_db'
}

def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Exception as e:
        print("DB connection error:", e)
        return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

# --- main app routes ---
@app.route('/')
def home():
    conn = get_db_connection()
    stats = {'total':'--','open':'--','closed':'--'}
    priority_counts = {'Critical':0,'High':0,'Medium':0,'Low':0}
    recent = []
    if conn:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT COUNT(*) total FROM tickets"); stats['total']=cur.fetchone()['total']
        cur.execute("SELECT COUNT(*) open FROM tickets WHERE status='Open'"); stats['open']=cur.fetchone()['open']
        cur.execute("SELECT COUNT(*) closed FROM tickets WHERE status='Closed'"); stats['closed']=cur.fetchone()['closed']
        cur.execute("SELECT priority, COUNT(*) cnt FROM tickets GROUP BY priority")
        for r in cur.fetchall():
            priority_counts[r['priority']] = r['cnt']
        cur.execute("SELECT ticket_id, employee_name, issue, issue_category, priority, status, created_at FROM tickets ORDER BY ticket_id DESC LIMIT 10")
        recent = cur.fetchall()
        cur.close(); conn.close()
    return render_template('home.html', stats=stats, pr_counts=json.dumps(priority_counts), recent=recent)

@app.route('/new_ticket', methods=['GET','POST'])
def new_ticket():
    message=None; priority='Low'; category='Other IT'
    if request.method == 'POST':
        issue = request.form.get('issue','').strip()
        employee = request.form.get('employee','').strip()
        role = request.form.get('role','customer').strip()
        # classification (simple)
        txt = issue.lower()
        if any(w in txt for w in ['server down','vpn','crash','outage','database']): base='Critical'
        elif any(w in txt for w in ['error','failed','denied','timeout','slow']): base='High'
        elif any(w in txt for w in ['not working','problem','issue','trouble','setup','install','config']): base='Medium'
        else: base='Low'
        if 'password' in txt or 'login' in txt or 'access' in txt: category='Access'
        elif 'email' in txt: category='Email'
        elif 'printer' in txt: category='Printer'
        elif 'network' in txt or 'wifi' in txt: category='Network'
        elif 'database' in txt: category='Database'
        order = ['Low','Medium','High','Critical']
        idx = order.index(base) if base in order else 0
        if role.lower() in ['vip','admin']: idx = min(idx+1, len(order)-1)
        priority = order[idx]
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO tickets (issue, employee_name, issue_category, priority, target_resolution_hours, status) VALUES (%s,%s,%s,%s,%s,%s)",
                            (issue, employee, category, priority, 24, 'Open'))
                conn.commit(); cur.close(); conn.close()
                message = f'Ticket created. Priority: {priority} (base {base})'
            except Exception as e:
                message = f'DB insert failed: {e}'
        else:
            message = f'Classified as {category}/{priority}. (DB unreachable)'
    return render_template('new_ticket.html', message=message, priority=priority, category=category)

@app.route('/tickets')
def tickets():
    conn = get_db_connection()
    rows = []
    if conn:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT ticket_id, employee_name, issue, issue_category, priority, status, created_at FROM tickets ORDER BY ticket_id DESC LIMIT 1000")
        rows = cur.fetchall()
        cur.close(); conn.close()
    return render_template('tickets.html', tickets=rows)


@app.route('/ticket/<int:ticket_id>')
def ticket_detail(ticket_id):
    conn = get_db_connection(); ticket=None; attachments=[]
    if conn:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM tickets WHERE ticket_id=%s",(ticket_id,)); ticket = cur.fetchone()
        cur.execute("SELECT attachment_id, file_name, file_path, uploaded_by, uploaded_at FROM attachments WHERE ticket_id=%s ORDER BY uploaded_at DESC",(ticket_id,)); attachments = cur.fetchall()
        cur.close(); conn.close()
    return render_template('ticket_detail.html', ticket=ticket, attachments=attachments)

@app.route('/ticket/<int:ticket_id>/upload', methods=['POST'])
def upload_file(ticket_id):
    if 'file' not in request.files:
        flash('No file part'); return redirect(url_for('ticket_detail', ticket_id=ticket_id))
    file = request.files['file']; uploader = request.form.get('uploader','unknown')[:100]
    if file.filename == '':
        flash('No chosen file'); return redirect(url_for('ticket_detail', ticket_id=ticket_id))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename); unique = f"{int(time.time())}_{filename}"; dest = os.path.join(app.config['UPLOAD_FOLDER'], unique)
        file.save(dest)
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO attachments (ticket_id, file_name, file_path, uploaded_by) VALUES (%s,%s,%s,%s)",
                            (ticket_id, filename, unique, uploader))
                conn.commit(); cur.close(); conn.close(); flash('File uploaded')
            except Exception as e:
                flash('DB insert for attachment failed: '+str(e))
        else:
            flash('File saved but DB unreachable')
    else:
        flash('File type not allowed')
    return redirect(url_for('ticket_detail', ticket_id=ticket_id))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/ticket/<int:ticket_id>/status', methods=['POST'])
def change_status(ticket_id):
    new_status = request.form.get('new_status')
    if new_status not in ('Open','In Progress','Resolved','Closed'):
        flash('Invalid status'); return redirect(url_for('ticket_detail', ticket_id=ticket_id))
    conn = get_db_connection()
    if not conn:
        flash('DB unreachable'); return redirect(url_for('ticket_detail', ticket_id=ticket_id))
    cur = conn.cursor()
    if new_status in ('Resolved','Closed'):
        cur.execute("UPDATE tickets SET status=%s, resolved_at=NOW() WHERE ticket_id=%s", (new_status, ticket_id))
    else:
        cur.execute("UPDATE tickets SET status=%s, resolved_at=NULL WHERE ticket_id=%s", (new_status, ticket_id))
    conn.commit(); cur.close(); conn.close(); flash('Status updated to '+new_status)
    return redirect(url_for('ticket_detail', ticket_id=ticket_id))

@app.route('/api/tickets/summary')
def api_summary():
    conn = get_db_connection(); data={'priority':{}, 'status':{}}
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT priority, COUNT(*) FROM tickets GROUP BY priority")
        for p,c in cur: data['priority'][p]=c
        cur.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status")
        for s,c in cur: data['status'][s]=c
        cur.close(); conn.close()
    return jsonify(data)

@app.route('/api/tickets/recent')
def api_recent_tickets():
    conn = get_db_connection()
    result = []
    if conn:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT ticket_id, employee_name, issue, priority, status, created_at FROM tickets ORDER BY ticket_id DESC LIMIT 10")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for r in rows:
            result.append({
                "ticket_id": r['ticket_id'],
                "employee_name": r['employee_name'],
                "issue": r['issue'],
                "priority": r['priority'],
                "status": r['status'],
                "created_at": str(r['created_at'])
            })
    return jsonify(recent=result)


if __name__=='__main__':
    app.run(debug=True)
