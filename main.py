from flask import Flask, render_template, url_for, request, redirect
import uuid
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/announcements")
def announce():
    return render_template("announce.html")

@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

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
        if 'form1' in request.form:
            # Handle form1 submission
            form1_data = request.form
            print("Form 1 data received:", form1_data)
            # Process form1_data as needed
            return redirect('/admin/control?token=' + token)

        elif 'form2' in request.form:
            # Handle form2 submission
            form2_data = request.form
            print("Form 2 data received:", form2_data)
            # Process form2_data as needed
            return redirect('/admin/control?token=' + token)


    return render_template("control.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)