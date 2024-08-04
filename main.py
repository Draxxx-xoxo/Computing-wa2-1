from flask import Flask, render_template, url_for, request, redirect
import uuid
import csv
app = Flask(__name__)

def readcsv(file_name):
    content = []
    with open(file_name, "r") as file:
         reader = csv.reader(file)
         for row in reader:
             content.append(row)
    return content
    
def addrow(file_name, new_row):
    with open(file_name, "a") as file:
        writer = csv.writer(file)
        writer.writerow(new_row)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/announcements")
def announce():
    homeworks = []
    events = []
    reminders = []
    with open("announcement.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == "homework":
                homeworks.append(row[1])
            elif row[0] == "event":
                events.append(row[1])
            else:
                 reminders.append(row[1])
                
    return render_template("announce.html", homeworks=homeworks, events=events, reminders=reminders)

@app.route("/attendance")
def attendance():
    content = readcsv("attendance.csv")
    with open("dates.txt", "r") as file:
        contents = file.readline()
        dates = contents.split(".")[:-1]
    return render_template("attendance.html", content=content, dates=dates)

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
                addrow("announcement.csv", ["homework", homework])

            if event:
                addrow("announcement.csv", ["event", event])
                
            if reminder:
                addrow("announcement.csv", ["reminder", reminder])

            return redirect('/admin/control?token=' + token)
        elif type == "student":
            name = request.form.get('name', '').strip()
            stu_class = request.form.get('class', '').strip()
            addrow("attendance.csv", [name, stu_class])
            with open("students.txt", "a") as file:
                file.write(name + ".")
            return redirect('/admin/control?token=' + token)
        elif type == "attendance":
            ab_day = request.form.get('ab_day', '').strip()
            month = request.form.get('month', '').strip()
            date = ab_day + "/" + month
            with open("dates.txt", "a") as file:
                file.write(date + ".")
            absent_students = request.form.getlist('absent_student')
            vr_students = request.form.getlist('vr_student')
            attendance_list = readcsv("attendance.csv")
            new_attendance_list = []
            for attendance in attendance_list:
                if attendance[0] in absent_students:
                    new_attendance_list.append(attendance + [0])
                elif attendance[0] in vr_students:
                    new_attendance_list.append(attendance + ["VR"])
                else:
                    new_attendance_list.append(attendance + [1])
            with open("attendance.csv", "w") as file:
                writer = csv.writer(file)
                for attendance in new_attendance_list:
                    writer.writerow(attendance)

            return redirect('/admin/control?token=' + token)
    with open("students.txt", "r") as file:
        contents = file.readline()
        student_name = contents.split(".")[:-1]
        
    
    return render_template("control.html", student_name=student_name)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)