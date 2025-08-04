from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_cors import CORS
import mysql.connector
import os
import random
import threading
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
CORS(app, supports_credentials=True, origins=['http://127.0.0.1:5000'])  # Explicitly allow origin

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Bhoomish@007',
    'database': 'daa'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def create_user_hashtable(role):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    role_mapping = {
        'student': 'student',
        'class advisor': 'class advisor',
        'hod': 'hod'
    }
    db_role = role_mapping.get(role.lower(), role)
    cursor.execute('SELECT email, password FROM users WHERE role = %s', (db_role,))
    users = cursor.fetchall()
    conn.close()
    return {user['email']: user['password'] for user in users}

def create_student_hashtable():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT student_id, name, email, department, year, dob, mobile, specialization, batch, campus, school FROM studinfo')
    students = cursor.fetchall()
    conn.close()
    return {student['email']: student for student in students}

def create_staff_hashtable(role):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT staff_id, name, email, department, mobile, campus, role, class FROM staffinfo WHERE role = %s', (role,))
    staff = cursor.fetchall()
    print(f"Staff for role '{role}': {staff}")  # Debug print
    conn.close()
    return {staff_member['email']: staff_member for staff_member in staff}

@app.route('/get_advisor_info', methods=['GET'])
def get_advisor_info():
    if 'email' not in session or 'role' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    email = session['email'].strip()  # Remove any whitespace
    role = session['role'].strip()
    
    if role.lower() != 'class advisor':
        return jsonify({'error': 'Access denied'}), 403
    
    advisor_hashtable = create_staff_hashtable('class advisor')
    print(f"Advisor hashtable: {advisor_hashtable}")  # Debug print
    if email in advisor_hashtable:
        return jsonify(advisor_hashtable[email])
    else:
        return jsonify({'error': 'Advisor info not found'}), 404
    
@app.route('/get_hod_info', methods=['GET'])
def get_hod_info():
    if 'email' not in session or 'role' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    email = session['email']
    role = session['role']
    
    if role != 'hod':
        return jsonify({'error': 'Access denied'}), 403
    
    hod_hashtable = create_staff_hashtable('hod')
    if email in hod_hashtable:
        return jsonify(hod_hashtable[email])
    else:
        return jsonify({'error': 'HOD info not found'}), 404

def move_approved_requests():
    while True:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT od_number, roll_number, from_time, to_time, date, reason, proof, teacher_approved, hod_approved, created_at
                FROM od_requests
                WHERE teacher_approved = 1 AND hod_approved = 1
            """
            cursor.execute(query)
            approved_requests = cursor.fetchall()

            for request in approved_requests:
                insert_query = """
                    INSERT INTO approved_od (od_number, roll_number, from_time, to_time, date, reason, proof, teacher_approved, hod_approved, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    request['od_number'],
                    request['roll_number'],
                    request['from_time'],
                    request['to_time'],
                    request['date'],
                    request['reason'],
                    request['proof'],
                    request['teacher_approved'],
                    request['hod_approved'],
                    request['created_at']
                ))
                delete_query = "DELETE FROM od_requests WHERE od_number = %s"
                cursor.execute(delete_query, (request['od_number'],))
                conn.commit()
                print(f"Moved OD {request['od_number']} to approved_od and deleted from od_requests")

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        time.sleep(20)

threading.Thread(target=move_approved_requests, daemon=True).start()

@app.route('/get_password', methods=['POST'])
def get_password():
    data = request.get_json()
    email = data.get('email')
    role = data.get('role')

    if not email or not role:
        return jsonify({'error': 'Email and role are required'}), 400

    user_hashtable = create_user_hashtable(role)
    
    if email in user_hashtable:
        password = user_hashtable[email]
        session['email'] = email
        session['role'] = role
        print(f"Session set in /get_password: {session}")
        return jsonify({'password': password})
    else:
        return jsonify({'error': 'User not found or role mismatch'}), 404

@app.route('/get_student_info', methods=['GET'])
def get_student_info():
    print(f"Session in /get_student_info: {session}")
    print(f"Cookies received: {request.cookies}")
    if 'email' not in session or 'role' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    email = session['email']
    role = session['role']
    
    if role != 'student':
        return jsonify({'error': 'Access denied'}), 403
    
    student_hashtable = create_student_hashtable()
    if email in student_hashtable:
        return jsonify(student_hashtable[email])
    else:
        return jsonify({'error': 'Student info not found'}), 404

@app.route('/get_pending_od_requests', methods=['GET'])
def get_pending_od_requests():
    if 'email' not in session or session.get('role') != 'student':
        return jsonify({'error': 'Not logged in'}), 401

    roll_number = request.args.get('roll_number')
    if not roll_number:
        return jsonify({'error': 'Roll number is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT od_number, reason, from_time, to_time, date, teacher_approved, hod_approved, created_at
            FROM od_requests
            WHERE roll_number = %s AND NOT (teacher_approved = 1 AND hod_approved = 1)
            ORDER BY created_at DESC
        """
        cursor.execute(query, (roll_number,))
        requests = cursor.fetchall()

        for req in requests:
            if isinstance(req['from_time'], (str, type(None))):
                pass
            else:
                req['from_time'] = str(req['from_time'])
            if isinstance(req['to_time'], (str, type(None))):
                pass
            else:
                req['to_time'] = str(req['to_time'])
            if req['date']:
                req['date'] = req['date'].strftime('%Y-%m-%d')
            if req['teacher_approved'] and req['hod_approved']:
                req['status'] = 'Level 2'
                req['final_status'] = 'Approved'
            elif req['teacher_approved']:
                req['status'] = 'Level 1'
                req['final_status'] = 'Pending'
            else:
                req['status'] = 'Level 0'
                req['final_status'] = 'Pending'
            req['created_on'] = req['created_at'].strftime('%d-%m-%Y')
            req['od_id'] = req['od_number']

        cursor.close()
        conn.close()
        return jsonify(requests)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Failed to fetch OD requests'}), 500

@app.route('/get_approved_od_requests', methods=['GET'])
def get_approved_od_requests():
    roll_number = request.args.get('roll_number')
    if not roll_number:
        return jsonify({'error': 'Roll number is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT od_number, reason, from_time, to_time, date, teacher_approved, hod_approved, created_at
            FROM approved_od
            WHERE roll_number = %s
            ORDER BY created_at DESC
        """
        cursor.execute(query, (roll_number,))
        requests = cursor.fetchall()

        for req in requests:
            if isinstance(req['from_time'], (str, type(None))):
                pass
            else:
                req['from_time'] = str(req['from_time'])
            if isinstance(req['to_time'], (str, type(None))):
                pass
            else:
                req['to_time'] = str(req['to_time'])
            if req['date']:
                req['date'] = req['date'].strftime('%Y-%m-%d')
            req['created_on'] = req['created_at'].strftime('%d-%m-%Y')
            req['od_id'] = req['od_number']

        cursor.close()
        conn.close()
        return jsonify(requests)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Failed to fetch approved OD requests'}), 500

@app.route('/get_hod_pending_od_requests', methods=['GET'])
def get_hod_pending_od_requests():
    if 'email' not in session or session.get('role') != 'hod':
        return jsonify({'error': 'Not logged in or unauthorized'}), 401

    email = session['email']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch the HOD's department
        cursor.execute('SELECT department FROM staffinfo WHERE email = %s AND role = "hod"', (email,))
        hod = cursor.fetchone()
        if not hod or not hod['department']:
            return jsonify({'error': 'HOD department not found'}), 404
        
        hod_department = hod['department']

        # Fetch pending OD requests where teacher_approved = 1 and hod_approved = 0, matching department
        query = """
            SELECT od.od_number, od.roll_number, od.reason, od.from_time, od.to_time, od.date, od.proof, od.teacher_approved, od.hod_approved, od.created_at
            FROM od_requests od
            JOIN studinfo s ON od.roll_number = s.student_id
            WHERE od.teacher_approved = 1 AND od.hod_approved = 0
            AND s.department = %s
            ORDER BY od.created_at DESC
        """
        cursor.execute(query, (hod_department,))
        requests = cursor.fetchall()

        for req in requests:
            req['from_time'] = str(req['from_time']) if req['from_time'] else None
            req['to_time'] = str(req['to_time']) if req['to_time'] else None
            req['date'] = req['date'].strftime('%Y-%m-%d') if req['date'] else None
            req['od_id'] = req['od_number']
            req['created_on'] = req['created_at'].strftime('%d-%m-%Y') if req['created_at'] else None
            if req['teacher_approved'] and req['hod_approved']:
                req['status'] = 'Level 2'
                req['final_status'] = 'Approved'
            elif req['teacher_approved']:
                req['status'] = 'Level 1'
                req['final_status'] = 'Pending'
            else:
                req['status'] = 'Level 0'
                req['final_status'] = 'Pending'

        cursor.close()
        conn.close()
        return jsonify(requests)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Failed to fetch pending OD requests'}), 500

@app.route('/get_hod_approved_od_requests', methods=['GET'])
def get_hod_approved_od_requests():
    if 'email' not in session or session.get('role') != 'hod':
        return jsonify({'error': 'Not logged in or unauthorized'}), 401

    email = session['email']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch the HOD's department
        cursor.execute('SELECT department FROM staffinfo WHERE email = %s AND role = "hod"', (email,))
        hod = cursor.fetchone()
        if not hod or not hod['department']:
            return jsonify({'error': 'HOD department not found'}), 404
        
        hod_department = hod['department']

        # Fetch fully approved requests from approved_od (Level 2)
        query_approved = """
            SELECT od.od_number, od.roll_number, od.reason, od.from_time, od.to_time, od.date, od.teacher_approved, od.hod_approved, od.created_at
            FROM approved_od od
            JOIN studinfo s ON od.roll_number = s.student_id
            WHERE s.department = %s
            ORDER BY od.created_at DESC
        """
        cursor.execute(query_approved, (hod_department,))
        approved_requests = cursor.fetchall()

        # Process the requests
        for req in approved_requests:
            req['from_time'] = str(req['from_time']) if req['from_time'] else None
            req['to_time'] = str(req['to_time']) if req['to_time'] else None
            req['date'] = req['date'].strftime('%Y-%m-%d') if req['date'] else None
            req['od_id'] = req['od_number']
            req['created_on'] = req['created_at'].strftime('%d-%m-%Y') if req['created_at'] else None
            req['status'] = 'Level 2'
            req['final_status'] = 'Approved'

        cursor.close()
        conn.close()
        return jsonify(approved_requests)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Failed to fetch approved OD requests'}), 500

@app.route('/approve_od_request', methods=['POST'])
def approve_od_request():
    if 'email' not in session or session.get('role') not in ['class advisor', 'hod']:
        return jsonify({'error': 'Not logged in or unauthorized'}), 401

    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    od_number = data.get('od_number')
    if not od_number:
        return jsonify({'error': 'OD number is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if session.get('role') == 'class advisor':
            query = "UPDATE od_requests SET teacher_approved = 1 WHERE od_number = %s AND teacher_approved = 0"
        else:  # hod
            query = "UPDATE od_requests SET hod_approved = 1 WHERE od_number = %s AND hod_approved = 0"
        cursor.execute(query, (od_number,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()

        if affected_rows > 0:
            return jsonify({'message': f'OD request {session.get("role")} approved successfully'})
        else:
            return jsonify({'error': 'OD request not found or already approved'}), 404
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Failed to approve OD request'}), 500

@app.route('/reject_od_request', methods=['POST'])
def reject_od_request():
    print("Debug: Entering reject_od_request")
    if 'email' not in session or session.get('role') not in ['class advisor', 'hod']:
        return jsonify({'error': 'Not logged in or unauthorized'}), 401

    data = request.get_json(silent=True)
    print(f"Debug: Data received: {data}")
    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    od_number = data.get('od_number')
    if not od_number:
        return jsonify({'error': 'OD number is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Adjust condition based on role
        if session.get('role') == 'class advisor':
            condition = "teacher_approved = 0"
        else:  # hod
            condition = "teacher_approved = 1 AND hod_approved = 0"

        query = f"SELECT * FROM od_requests WHERE od_number = %s AND {condition}"
        cursor.execute(query, (od_number,))
        request_db = cursor.fetchone()

        if not request_db:
            return jsonify({'error': 'OD request not found or already processed'}), 404

        # Move to reject_od, using the original created_at or NULL if not present
        insert_query = """
            INSERT INTO reject_od (od_number, roll_number, from_time, to_time, date, reason, proof, teacher_approved, hod_approved, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            request_db['od_number'],
            request_db['roll_number'],
            request_db['from_time'],
            request_db['to_time'],
            request_db['date'],
            request_db['reason'],
            request_db['proof'],
            request_db['teacher_approved'],
            request_db['hod_approved'],
            request_db['created_at'] if request_db['created_at'] else None
        ))

        # Delete from od_requests
        delete_query = "DELETE FROM od_requests WHERE od_number = %s"
        cursor.execute(delete_query, (od_number,))
        conn.commit()
        affected_rows = cursor.rowcount

        cursor.close()
        conn.close()

        if affected_rows > 0:
            return jsonify({'message': 'OD request rejected successfully'})
        else:
            return jsonify({'error': 'Failed to delete OD request'}), 500
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Failed to reject OD request'}), 500

@app.route('/')
def index_page():
    return app.send_static_file('index.html')

@app.route('/login')
def login_page():
    print(f"Session in /login: {session}")
    return app.send_static_file('login.html')

@app.route('/login_redirect', methods=['POST'])
def login_redirect():
    email = request.form.get('email')
    role = request.form.get('role')
    password = request.form.get('password')
    
    user_hashtable = create_user_hashtable(role)
    if email in user_hashtable and user_hashtable[email] == password:
        session['email'] = email
        session['role'] = role
        print(f"Session set in /login_redirect: {session}")
        if role == 'student':
            return redirect(url_for('student_dashboard'))
        elif role == 'class advisor':
            return redirect(url_for('advisor_dashboard'))
        elif role == 'hod':
            return redirect(url_for('hod_dashboard'))
    return redirect(url_for('login_page'))

@app.route('/dashboard/student')
def student_dashboard():
    print(f"Session in /dashboard/student: {session}")
    if 'email' not in session or session.get('role') != 'student':
        return redirect(url_for('login_page'))
    return app.send_static_file('student_dashboard.html')

@app.route('/submit_od')
def submit_od():
    print(f"Session in /submit_od: {session}")
    if 'email' not in session or session.get('role') != 'student':
        return redirect(url_for('login_page'))
    return app.send_static_file('submit_od.html')

@app.route('/submit_od_request', methods=['POST'])
def submit_od_request():
    if 'email' not in session or session.get('role') != 'student':
        return jsonify({'error': 'Not logged in'}), 401

    roll_number = request.form.get('roll_number')
    from_time = request.form.get('from_time')
    to_time = request.form.get('to_time')
    date = request.form.get('date')
    reason = request.form.get('reason')
    proof = request.form.get('proof')

    if not all([roll_number, from_time, to_time, date, reason, proof]):
        return jsonify({'error': 'All fields are required'}), 400

    if to_time <= from_time:
        return jsonify({'error': 'To Time must be after From Time'}), 400

    random_id = random.randint(1000, 9999)
    od_number = f"OD{random_id}"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO od_requests (od_number, roll_number, from_time, to_time, date, reason, proof, teacher_approved, hod_approved)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (od_number, roll_number, from_time, to_time, date, reason, proof, False, False)
        cursor.execute(query, values)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Failed to save OD request'}), 500
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('student_dashboard') + '?success=true')

@app.route('/get_advisor_pending_od_requests', methods=['GET'])
def get_advisor_pending_od_requests():
    if 'email' not in session or session.get('role') != 'class advisor':
        return jsonify({'error': 'Not logged in or unauthorized'}), 401

    email = session['email']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT class FROM staffinfo WHERE email = %s AND role = "class advisor"', (email,))
        advisor = cursor.fetchone()
        if not advisor or not advisor['class']:
            return jsonify({'error': 'Advisor class not found'}), 404
        
        advisor_class = advisor['class']

        query = """
            SELECT od.od_number, od.roll_number, od.reason, od.from_time, od.to_time, od.date, od.proof, od.teacher_approved, od.hod_approved, od.created_at
            FROM od_requests od
            JOIN studinfo s ON od.roll_number = s.student_id
            WHERE od.teacher_approved = 0 AND od.hod_approved = 0
            AND s.batch LIKE %s
            ORDER BY od.created_at DESC
        """
        cursor.execute(query, (f'%{advisor_class}%',))
        requests = cursor.fetchall()

        for req in requests:
            req['from_time'] = str(req['from_time']) if req['from_time'] else None
            req['to_time'] = str(req['to_time']) if req['to_time'] else None
            req['date'] = req['date'].strftime('%Y-%m-%d') if req['date'] else None
            req['od_id'] = req['od_number']
            req['created_on'] = req['created_at'].strftime('%d-%m-%Y') if req['created_at'] else None
            if req['teacher_approved'] and req['hod_approved']:
                req['status'] = 'Level 2'
                req['final_status'] = 'Approved'
            elif req['teacher_approved']:
                req['status'] = 'Level 1'
                req['final_status'] = 'Pending'
            else:
                req['status'] = 'Level 0'
                req['final_status'] = 'Pending'

        cursor.close()
        conn.close()
        return jsonify(requests)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Failed to fetch pending OD requests'}), 500

@app.route('/get_advisor_approved_od_requests', methods=['GET'])
def get_advisor_approved_od_requests():
    if 'email' not in session or session.get('role') != 'class advisor':
        return jsonify({'error': 'Not logged in or unauthorized'}), 401

    email = session['email']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch the advisor's class
        cursor.execute('SELECT class FROM staffinfo WHERE email = %s AND role = "class advisor"', (email,))
        advisor = cursor.fetchone()
        if not advisor or not advisor['class']:
            return jsonify({'error': 'Advisor class not found'}), 404
        
        advisor_class = advisor['class']

        # Query 1: Fetch fully approved requests from approved_od (Level 2)
        query_approved = """
            SELECT od.od_number, od.roll_number, od.reason, od.from_time, od.to_time, od.date, od.teacher_approved, od.hod_approved, od.created_at, 'approved_od' as source
            FROM approved_od od
            JOIN studinfo s ON od.roll_number = s.student_id
            WHERE s.batch LIKE %s
        """
        cursor.execute(query_approved, (f'%{advisor_class}%',))
        approved_requests = cursor.fetchall()

        # Query 2: Fetch advisor-approved but not HOD-approved requests from od_requests (Level 1, pending)
        query_pending = """
            SELECT od.od_number, od.roll_number, od.reason, od.from_time, od.to_time, od.date, od.teacher_approved, od.hod_approved, od.created_at, 'od_requests' as source
            FROM od_requests od
            JOIN studinfo s ON od.roll_number = s.student_id
            WHERE od.teacher_approved = 1 AND od.hod_approved = 0
            AND s.batch LIKE %s
        """
        cursor.execute(query_pending, (f'%{advisor_class}%',))
        pending_requests = cursor.fetchall()

        # Query 3: Fetch advisor-approved but HOD-rejected requests from reject_od (Level 1, rejected)
        query_rejected = """
            SELECT od.od_number, od.roll_number, od.reason, od.from_time, od.to_time, od.date, od.teacher_approved, od.hod_approved, od.created_at, 'reject_od' as source
            FROM reject_od od
            JOIN studinfo s ON od.roll_number = s.student_id
            WHERE od.teacher_approved = 1 AND od.hod_approved = 0
            AND s.batch LIKE %s
        """
        cursor.execute(query_rejected, (f'%{advisor_class}%',))
        rejected_requests = cursor.fetchall()

        # Combine the requests
        all_requests = approved_requests + pending_requests + rejected_requests

        # Process the combined requests
        for req in all_requests:
            req['from_time'] = str(req['from_time']) if req['from_time'] else None
            req['to_time'] = str(req['to_time']) if req['to_time'] else None
            req['date'] = req['date'].strftime('%Y-%m-%d') if req['date'] else None
            req['od_id'] = req['od_number']
            req['created_on'] = req['created_at'].strftime('%d-%m-%Y') if req['created_at'] else None
            # Set status and final_status based on the source
            if req['source'] == 'approved_od':
                req['status'] = 'Level 2'
                req['final_status'] = 'Approved'
            elif req['source'] == 'od_requests':
                req['status'] = 'Level 1'
                req['final_status'] = 'Pending'
            else:  # reject_od
                req['status'] = 'Level 1'
                req['final_status'] = 'Rejected'

        # Sort by created_at in descending order (newest to oldest)
        all_requests.sort(key=lambda x: x['created_at'] or '1970-01-01 00:00:00', reverse=True)

        cursor.close()
        conn.close()
        return jsonify(all_requests)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Failed to fetch approved OD requests'}), 500

@app.route('/dashboard/advisor')
def advisor_dashboard():
    print(f"Session in /dashboard/advisor: {session}")
    if 'email' not in session or session.get('role') != 'class advisor':
        return redirect(url_for('login_page'))
    return app.send_static_file('advisor_dashboard.html')

@app.route('/dashboard/hod')
def hod_dashboard():
    print(f"Session in /dashboard/hod: {session}")
    if 'email' not in session or session.get('role') != 'hod':
        return redirect(url_for('login_page'))
    return app.send_static_file('hod_dashboard.html')

@app.route('/get_all_past_od_requests', methods=['GET'])
def get_all_past_od_requests():
    if 'email' not in session or session.get('role') != 'student':
        return jsonify({'error': 'Not logged in'}), 401

    roll_number = request.args.get('roll_number')
    if not roll_number:
        return jsonify({'error': 'Roll number is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch from both approved_od and reject_od tables
        queries = [
            """
            SELECT od_number as od_id, reason, from_time, to_time, date, teacher_approved, hod_approved, created_at, 'approved_od' as table_name
            FROM approved_od
            WHERE roll_number = %s
            """,
            """
            SELECT od_number as od_id, reason, from_time, to_time, date, teacher_approved, hod_approved, created_at, 'reject_od' as table_name
            FROM reject_od
            WHERE roll_number = %s
            """
        ]

        all_requests = []
        for query in queries:
            cursor.execute(query, (roll_number,))
            requests = cursor.fetchall()
            for req in requests:
                req['from_time'] = str(req['from_time']) if req['from_time'] else None
                req['to_time'] = str(req['to_time']) if req['to_time'] else None
                req['date'] = req['date'].strftime('%Y-%m-%d') if req['date'] else None
                req['created_on'] = req['created_at'].strftime('%d-%m-%Y') if req['created_at'] else None

            all_requests.extend(requests)

        # Sort by created_at (newest to oldest) for accurate ordering
        all_requests.sort(key=lambda x: x['created_at'] or '1970-01-01 00:00:00', reverse=True)

        cursor.close()
        conn.close()
        return jsonify(all_requests)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Failed to fetch all past OD requests'}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)