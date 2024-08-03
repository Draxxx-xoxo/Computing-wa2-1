from flask import Flask, render_template, url_for, request, redirect

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
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)