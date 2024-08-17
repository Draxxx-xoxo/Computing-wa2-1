from flask import Flask, render_template, url_for, request, redirect
import uuid
import sqlite3
import bcrypt
import json
app = Flask(__name__)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
def get_password():
    with open("password.json", 'r') as file:
        data = json.load(file)
    return data['password'].encode('utf-8')

def set_password(new_password):
    hashed_password = hash_password(new_password)
    with open("password.json", 'w') as file:
        json.dump({'password': hashed_password.decode('utf-8')}, file)
    
def opendb(query, params=None):
    con = sqlite3.connect('activity_hub.db')
    cur = con.cursor()
    if params is None:
        cur.execute(query)
    else:
        cur.execute(query, params)
    res = cur.fetchall()
    con.close()
    return res

def editdb(query, values):
    con = sqlite3.connect('activity_hub.db')
    cur = con.cursor()
    cur.execute(query, values)
    con.commit()
    con.close()

def addcolumn(command):
    conn = sqlite3.connect('activity_hub.db')
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()
    conn.close()

def delete_rows_by_ids(table_name, column_name, ids):
    con = sqlite3.connect('activity_hub.db')
    cur = con.cursor()
    for id in ids:
        delete_query = f"DELETE FROM {table_name} WHERE {column_name} = ?;"
        cur.execute(delete_query, (id,))
    con.commit()
    con.close()
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        message = request.form.get('message')
        with open("messages.txt", "a") as file:
            file.write(message + "\n")
        return redirect(url_for('home'))
    else: 
        messages = []
        with open("messages.txt", "r") as file:
            content = file.readlines()
            for line in content:
                messages.append(line.rstrip())
        return render_template("index.html", messages=messages)

@app.route("/announcements")
def announce():
    homeworks = opendb("SELECT announcement_id, announcement FROM announcements WHERE type = ?", ('homework',))
    events = opendb("SELECT announcement_id, announcement FROM announcements WHERE type = ?", ('event',))
    reminders = opendb("SELECT announcement_id, announcement FROM announcements WHERE type = ?", ('reminder',))
               
    return render_template("announce.html", homeworks=homeworks, events=events, reminders=reminders)

@app.route("/attendance")
def attendance():
    data = opendb("SELECT * FROM attendance")
    
    con = sqlite3.connect('activity_hub.db')
    cur = con.cursor()
    query = "SELECT * FROM attendance LIMIT 1"
    cur.execute(query)
    dates = [description[0] for description in cur.description]
    formatted_dates = []
    for date in dates[3:]:
        formatted_dates.append(date.replace('_', '-'))
    dates = formatted_dates       
    con.close()
    return render_template("attendance.html", data=data, dates=dates)

@app.route("/schedule")
def schedule():
    data = opendb("SELECT * FROM schedule", None)
    return render_template("schedule.html", data=data)

tokens = {}

@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        stored_password_hash = get_password()
        if stored_password_hash and bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            token = str(uuid.uuid4())
            tokens[token] = True
            return redirect(f'/admin/control?token={token}')
        else:
            return redirect('/admin?error=True')

    token = request.args.get('token')
    if token in tokens:
        access = True
    else:
        access = False
        if request.args.get('logout'):
            tokens.pop(token, None)
    with open("for_access.txt", "r") as file:
        pw = file.readline()

    return render_template("admin.html", access=access, pw=pw)

@app.route("/logout")
def logout():
    return redirect('/admin?logout=true')

@app.route("/admin/control", methods=["GET", "POST"])
def admin_dashboard():
    token = request.args.get('token')
    if token not in tokens:
        return redirect('/admin?error=True')

    if request.method == "POST":
        type = request.form.get('type')
        if type == "announcement":
            homework = request.form.get('homework', '').strip()
            event = request.form.get('event', '').strip()
            reminder = request.form.get('reminder', '').strip()

            if homework:
                editdb("INSERT INTO announcements (type, announcement) VALUES (?, ?)", ("homework", homework))

            if event:
                editdb("INSERT INTO announcements (type, announcement) VALUES (?, ?)", ("event", event))
                
            if reminder:
                editdb("INSERT INTO announcements (type, announcement) VALUES (?, ?)", ("reminder", reminder))

            return redirect(url_for('admin_dashboard', token=token))
        elif type == "delete_announcement":
            ids = [int(id) for id in request.form.getlist('delete_announcement')]
            delete_rows_by_ids("announcements", "announcement_id", ids)
            
            return redirect(url_for('admin_dashboard', token=token))
        elif type == "student":
            name = request.form.get('name', '').strip()
            stu_class = request.form.get('class', '').strip()
            editdb("INSERT INTO attendance (name, class) VALUES (?, ?)", (name, stu_class))
            return redirect(url_for('admin_dashboard', token=token))
        elif type == "delete_student":
            ids = [int(id) for id in request.form.getlist('delete_student')]
            delete_rows_by_ids("attendance", "stu_id", ids)
            return redirect(url_for('admin_dashboard', token=token))
        elif type == "attendance":
            original_date = request.form.get('ab_date', '').strip()
            ori_date = original_date.replace('-', '_')
            date = f"'{ori_date}'"
            con = sqlite3.connect('activity_hub.db')
            cur = con.cursor()
            cur.execute("PRAGMA table_info(attendance)")
            columns = [row[1] for row in cur.fetchall()]
            con.close()
            
            if ori_date not in columns:
                addcolumn(f"ALTER TABLE attendance ADD COLUMN {date} TEXT;")
            editdb(f"UPDATE attendance SET {date} = ?", ('1',))
            absent_students = request.form.getlist('absent_student')
            vr_students = request.form.getlist('vr_student')
            for student in absent_students:
                editdb(f"UPDATE attendance SET {date} = ? WHERE stu_id = ?", ('0', student))

            for student in vr_students:
                editdb(f"UPDATE attendance SET {date} = ? WHERE stu_id = ?", ('VR', student))
            return redirect(url_for('admin_dashboard', token=token))
        elif type == "schedule":
            term = request.form.get('term', '').strip()
            week = request.form.get('week', '').strip()
            date = request.form.get('date', '').strip()
            day = request.form.get('day', '').strip()
            session = request.form.get('session', '').strip()
            start = request.form.get('start', '').strip()
            end = request.form.get('end', '').strip()
            remark = request.form.get('remark', '').strip()
            editdb("INSERT INTO schedule (term, week, date, day, session, start, end, remark) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (term, week, date, day, session, start, end, remark))
            return redirect(url_for('admin_dashboard', token=token))
        elif type == "delete_schedule":
            ids = [int(id) for id in request.form.getlist('delete_schedule')]
            delete_rows_by_ids("schedule", "schedule_id", ids)
            return redirect(url_for('admin_dashboard', token=token))
        elif type == "password":
            new_pw = request.form.get('new_pw')
            with open("for_access.txt", "w") as file:
                file.write(new_pw)
            set_password(new_pw)            
            return redirect(url_for('admin'))
        elif type == "clear_msg":
            with open("messages.txt", "w") as file:
                pass
            return redirect(url_for('home'))
    student_name = opendb("SELECT stu_id, name, class FROM attendance", None)
    announcements = opendb("SELECT announcement_id, announcement FROM announcements", None)
    schedules = opendb("SELECT * FROM schedule", None)
    return render_template("control.html", student_name=student_name, announcements=announcements, schedules=schedules)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)