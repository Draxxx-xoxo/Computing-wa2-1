from flask import Flask, render_template, url_for, request, redirect
import uuid
import sqlite3
app = Flask(__name__)

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


@app.route("/")
def home():
    return render_template("index.html")

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
        split_date = date.split("_")
        formatted_dates.append(split_date[0] + "/" + split_date[1])
    dates = formatted_dates       
    con.close()
    return render_template("attendance.html", data=data, dates=dates)

@app.route("/schedule")
def schedule():
    return render_template("schedule.html")

tokens = {}

@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "Admin12345":
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

    return render_template("admin.html", access=access)

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

            return redirect('/admin/control?token=' + token)
        elif type == "student":
            name = request.form.get('name', '').strip()
            stu_class = request.form.get('class', '').strip()
            editdb("INSERT INTO attendance (name, class) VALUES (?, ?)", (name, stu_class))
            return redirect('/admin/control?token=' + token)
        elif type == "attendance":
            ab_day = request.form.get('ab_day', '').strip()
            month = request.form.get('month', '').strip()
            date = ab_day + "_" + month
            date = f"'{date}'"
            addcolumn((f"ALTER TABLE attendance ADD COLUMN {date} TEXT;"))
            absent_students = request.form.getlist('absent_student')
            vr_students = request.form.getlist('vr_student')
            editdb(f"UPDATE attendance SET {date} = ?", ('1',))
            for student in absent_students:
                editdb(f"UPDATE attendance SET {date} = ? WHERE name = ?", ('0', student))
            for student in vr_students:
                editdb(f"UPDATE attendance SET {date} = ? WHERE name = ?", ('VR', student))
            return redirect('/admin/control?token=' + token)

    student_name = opendb("SELECT name, class FROM attendance", None)
   
    return render_template("control.html", student_name=student_name)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)