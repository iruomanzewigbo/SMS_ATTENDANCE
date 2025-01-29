import sqlite3
from flask import Flask,redirect,url_for, request, render_template, jsonify
import config
import time

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT,
                    student_name TEXT,
                    timestamp TEXT
                 )''')
    conn.commit()
    conn.close()

# Function to add attendance record
def mark_attendance(student_id, student_name):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO attendance (student_id, student_name, timestamp) VALUES (?, ?, ?)", 
              (student_id, student_name, timestamp))
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/attendance", methods=["POST"])
def mark_attendance_route():
    student_id = request.form['student_id']
    student_name = request.form['student_name']

    if student_id and student_name:
        mark_attendance(student_id, student_name)
        return f"Attendance marked for {student_name} (ID: {student_id})"
    else:
        return "Error: Missing student ID or name!"

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT,debug=True)
