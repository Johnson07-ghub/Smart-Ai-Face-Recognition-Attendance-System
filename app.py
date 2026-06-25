from flask import Flask, render_template, Response, jsonify, request, redirect, session
import cv2
import sqlite3
from datetime import datetime
import pickle
import pandas as pd
import os
import face_recognition
import numpy as np

app = Flask(__name__)
app.secret_key = "attendance_secret_key"

# ================= DATABASE =================

conn = sqlite3.connect("attendance.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    name TEXT,
    time TEXT
)
""")

conn.commit()

# ================= LOAD MODEL =================

with open("trainer/encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
last_name = ""
stable_count = 0
required_frames = 3
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280 )
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# Prevent duplicate unknown entries
last_unknown_time = None

# ================= ATTENDANCE =================
def mark_attendance(name):

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if name == "Unknown Person":

        cursor.execute("""
        SELECT *
        FROM attendance
        WHERE name='Unknown Person'
        ORDER BY time DESC
        LIMIT 1
        """)

        last = cursor.fetchone()

        if last is None:

            cursor.execute("""
            INSERT INTO attendance(name,time)
            VALUES (?,?)
            """, (name, now))

        conn.commit()
        conn.close()
        return

    cursor.execute("""
    SELECT *
    FROM attendance
    WHERE name=?
    AND date(time)=date('now')
    """, (name,))

    if cursor.fetchone() is None:

        cursor.execute("""
        INSERT INTO attendance(name,time)
        VALUES (?,?)
        """, (name, now))

        conn.commit()

    conn.close()

# ================= VIDEO STREAM =================
def generate_frames():

    global last_name
    global stable_count
    global last_marked_name
    last_name = ""
    stable_count = 0
    required_frames = 3
    last_marked_name = ""

    while True:

        success, frame = camera.read()

        if not success:
            stable_count = 0
            last_name = ""
            continue

        frame = cv2.resize(
            frame,
            (0, 0),
            fx=0.5,
            fy=0.5
        )

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        face_locations = face_recognition.face_locations(
            rgb,
            number_of_times_to_upsample=1,
            model="hog"
        )

        face_encodings = face_recognition.face_encodings(
            rgb,
            face_locations
        )

        if len(face_encodings) == 0:
            stable_count = 0
            last_name = ""

        for face_encoding, face_location in zip(
            face_encodings,
            face_locations
        ):

            name = "Unknown Person"
            current_name = "Unknown Person"

            matches = face_recognition.compare_faces(
                known_encodings,
                face_encoding,
                tolerance=0.45
            )

            face_distances = face_recognition.face_distance(
                known_encodings,
                face_encoding
            )

            if len(face_distances) > 0:

                best_match = np.argmin(
                    face_distances
                )

                if (
                    matches[best_match]
                    and
                    face_distances[best_match] < 0.45
                ):

                    current_name = known_names[
                        best_match
                    ]

            if current_name == last_name:

                stable_count += 1

            else:

                stable_count = 1
                last_name = current_name

            if stable_count >= required_frames:

                name = current_name

                if (
                    name != "Unknown Person"
                    and
                    name != last_marked_name
                ):

                    mark_attendance(name)
                    last_marked_name = name

                elif name == "Unknown Person":
                    mark_attendance("Unknown Person")

            else:

                name = "Detecting..."

            top, right, bottom, left = face_location

            if name == "Unknown Person":
                color = (0, 0, 255)

            elif name == "Detecting...":
                color = (0, 255, 255)

            else:
                color = (0, 255, 0)

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                color,
                2
            )

            cv2.putText(
                frame,
                name,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )



# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":

            session["user"] = "admin"
            return redirect("/dashboard")

        return "Invalid Credentials"

    return render_template("login.html")

# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/home")

# ================= HOME =================
@app.route("/")
@app.route("/home")

def home():
    return render_template("home.html")
# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    print("SESSION =", session)

    if "user" not in session:
        return redirect("/login")

    conn_dash = sqlite3.connect("attendance.db")
    cursor_dash = conn_dash.cursor()

    # Recent Attendance
    cursor_dash.execute("""
    SELECT *
    FROM attendance
    ORDER BY time DESC
    """)
    records = cursor_dash.fetchall()

    # Present Today
    cursor_dash.execute("""
    SELECT COUNT(DISTINCT name)
    FROM attendance
    WHERE name!='Unknown Person'
    """)
    total_attendance = cursor_dash.fetchone()[0]

    # Total Students
    dataset_path = "DataSets"

    if os.path.exists(dataset_path):

        total_students = len([
            folder
            for folder in os.listdir(dataset_path)
            if os.path.isdir(
                os.path.join(dataset_path, folder)
            )
        ])

    else:
        total_students = 0

    # Unknown Faces
    cursor_dash.execute("""
    SELECT COUNT(*)
    FROM attendance
    WHERE name='Unknown Person'
    """)
    result = cursor_dash.fetchone()
    unknown_faces = result[0] if result else 0

    # AI Accuracy
    ai_accuracy = "90.5%"

    conn_dash.close()

    return render_template(
        "dashboard.html",
        records=records,
        total_students=total_students,
        total_attendance=total_attendance,
        unknown_faces=unknown_faces,
        ai_accuracy=ai_accuracy
    )
# ================= ATTENDANCE PAGE =================

@app.route("/attendance")
def attendance():

    if "user" not in session:
        return redirect("/login")

    cursor.execute("""
    SELECT *
    FROM attendance
    ORDER BY time DESC
    """)

    records = cursor.fetchall()

    return render_template(
        "attendance.html",
        records=records
    )



# ================= STUDENTS PAGE =================

@app.route("/students")
def students():

    if "user" not in session:
        return redirect("/login")

    dataset_path = "DataSets"

    student_list = []

    if os.path.exists(dataset_path):

        for folder in os.listdir(dataset_path):

            if os.path.isdir(os.path.join(dataset_path, folder)):
                student_list.append(folder)

    return render_template(
        "students.html",
        students=student_list
    )

# ================= SETTINGS PAGE =================

@app.route("/settings")
def settings():

    if "user" not in session:
        return redirect("/login")

    return render_template("settings.html")

# ================= VIDEO FEED =================

@app.route("/video")
def video():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# ================= API =================

@app.route("/api/attendance")
def api_attendance():

    cursor.execute("""
    SELECT *
    FROM attendance
    ORDER BY time DESC
    LIMIT 20
    """)

    data = cursor.fetchall()

    return jsonify({
        "records": [
            {
                "name": r[0],
                "time": r[1]
            }
            for r in data
        ]
    })

# ================= EXPORT =================

from flask import send_file

@app.route("/export")
def export():

    cursor.execute("SELECT * FROM attendance")

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=["Name", "Time"]
    )

    file_name = "attendance.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )
# ============= Reset attendance data ================
@app.route("/reset_unknown")
def reset_unknown():

    cursor.execute("""
    DELETE FROM attendance
    WHERE name='Unknown Person'
    """)

    conn.commit()

    return redirect("/dashboard")


@app.route("/reset_attendance")
def reset_attendance():

    cursor.execute("""
    DELETE FROM attendance
    """)

    conn.commit()

    return redirect("/dashboard")
# ================= RUN =================

if __name__ == "__main__":

    app.run(debug=False)