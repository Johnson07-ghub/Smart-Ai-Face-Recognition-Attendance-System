 🤖 Smart AI Face Recognition Attendance System

📌 Overview

Smart AI Face Recognition Attendance System is an intelligent attendance management application that automatically detects and recognizes students using facial recognition technology. The system captures live video from a webcam, identifies registered students in real time, and records attendance directly into a database without manual intervention.

🚀 Features

* Real-time face detection using webcam
* AI-powered face recognition
* Automatic attendance marking
* Unknown person detection
* Duplicate attendance prevention
* Live camera monitoring
* Attendance dashboard with statistics
* Student management system
* Attendance export to Excel
* Secure admin login authentication
* Attendance reset functionality
* Responsive web-based interface
* 
 🛠 Technologies Used:

 Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Jinja2 Templates

Backend :

* Python
* Flask Framework

Database :

* SQLite3

 Artificial Intelligence & Computer Vision :

* OpenCV
* Face Recognition Library
* dlib
* NumPy

Data Processing :

* Pandas
* Pickle


 🏗 System Architecture

1. Camera captures live video stream.
2. OpenCV processes video frames.
3. Face Detection identifies faces.
4. Face Recognition compares detected faces with trained encodings.
5. Recognized student names are matched.
6. Attendance is automatically stored in SQLite database.
7. Dashboard displays attendance records in real time.
8. Admin can monitor and export attendance reports.

-

 📂 Project Structure

Attendance_Project/

├── app.py

├── attendance.db

├── trainer/

│ └── encodings.pkl

├── DataSets/

│ ├── Student1/

│ ├── Student2/

│ └── ...

├── templates/

│ ├── home.html

│ ├── dashboard.html

│ ├── login.html

│ ├── attendance.html

│ ├── students.html

│ └── settings.html

├── static/

│ ├── style.css

│ └── script.js

└── README.md



 🔐 Authentication

Admin authentication is implemented using Flask Session Management.

Default Credentials:

Username: -------

Password: -------

 📊 Dashboard Functions

* Total Students Count
* Present Students Count
* AI Recognition Accuracy
* Unknown Face Count
* Live Camera Feed
* Recent Attendance Records
* System Status Monitoring

 📈 Future Enhancements

* Cloud Database Integration
* Email Notifications
* Mobile Application Support
* Multi-Camera Support
* Face Mask Detection
* Deep Learning Based Recognition
* Attendance Analytics Dashboard
* Role-Based Access Control


 ▶️ Installation

 Clone Repository

git clone https://github.com/your-username/Smart-AI-Face-Recognition-Attendance-System.git

Create Virtual Environment

python -m venv venv

 Activate Environment

Windows:

venv\Scripts\activate

 Install Dependencies

pip install -r requirements.txt

 Run Application

python app.py

 Open Browser

http://127.0.0.1:5000

 🎯 Project Outcome

The system successfully automates attendance management using Artificial Intelligence and Computer Vision techniques, reducing manual effort, improving accuracy, and providing real-time attendance monitoring through a user-friendly dashboard.

👨‍💻 Developer

Johnson

AI & Machine Learning Enthusiast

Python Developer

Computer Vision Projects
