from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
import io
import csv
import socket
import nmap
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

# Dummy login credentials
USER_CREDENTIALS = {'admin': 'vaptsecure123'}

# Decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error='❌ Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template('index.html', result='❌ No file selected')

    file = request.files['file']
    try:
        df = pd.read_csv(file)
        df['prediction'] = 'vulnerable'  # dummy prediction logic
        output = df.to_html(classes='table table-striped', index=False)
        return render_template('index.html', result="✅ Prediction Completed", table=output)
    except Exception as e:
        return render_template('index.html', result=f'❌ Error: {str(e)}')

@app.route('/scan_ip', methods=['POST'])
@login_required
def scan_ip():
    target = request.form['target']
    scanner = nmap.PortScanner()
    scan_data = []

    try:
        ip = socket.gethostbyname(target)
        scanner.scan(hosts=ip, arguments='-T4 -F')

        if ip in scanner.all_hosts():
            for proto in scanner[ip].all_protocols():
                for port in sorted(scanner[ip][proto].keys()):
                    state = scanner[ip][proto][port]['state']
                    row = {
                        'target': target,
                        'ip': ip,
                        'port': f"{port}/{proto}",
                        'status': state,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    scan_data.append(row)

                    with open('scan_logs.csv', 'a', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=row.keys())
                        if f.tell() == 0:
                            writer.writeheader()
                        writer.writerow(row)
        else:
            return render_template('index.html', result="❌ Target is unreachable or not responding.")

    except Exception as e:
        return render_template('index.html', result=f'❌ Scan failed: {str(e)}')

    return render_template('index.html', scan_table=scan_data)

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        df = pd.read_csv('scan_logs.csv', on_bad_lines='skip')
        total_scans = len(df)
        open_ports = df[df['status'] == 'open'].shape[0]
        closed_ports = df[df['status'] == 'closed'].shape[0]

        top_targets = df['target'].value_counts().head(5).to_dict() if 'target' in df.columns else {}
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        scans_by_date = df['timestamp'].dt.date.value_counts().sort_index()

        return render_template(
            'dashboard.html',
            total_scans=total_scans,
            open_ports=open_ports,
            closed_ports=closed_ports,
            top_targets=top_targets,
            scans_by_date=scans_by_date
        )
    except Exception as e:
        return f"Dashboard error: {str(e)}"

@app.route('/recent-scans')
@login_required
def recent_scans():
    try:
        df = pd.read_csv('scan_logs.csv', on_bad_lines='skip')
        scan_logs = df.to_dict(orient='records')
    except Exception:
        scan_logs = []
    return render_template('recent_scans.html', scan_logs=scan_logs)

@app.route('/download-scans')
@login_required
def download_scans():
    try:
        df = pd.read_csv('scan_logs.csv', on_bad_lines='skip')
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='recent_scans.csv'
        )
    except Exception as e:
        return f"Error: {str(e)}"

# ✅ Render deployment port setup
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
