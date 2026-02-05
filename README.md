# 📚 Attendance Management System

A simple and lightweight Django application for managing student attendance in small classes.
Designed for teachers to easily create sessions, mark absences, and track attendance records.

---

## ✨ Features

- Create and manage class sessions
- Mark student attendance/absence
- Admin dashboard for instructors
- Simple and clean interface
- Built with Django Admin customization
- Suitable for small schools, courses, and study groups

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10+
- Git

Check your Python version:

python --version

---

### 2. Installation

#### Clone the repository

git clone <your-repository-link>
cd upc_absence

#### Create virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

Mac / Linux:

python3 -m venv venv
source venv/bin/activate

#### Install dependencies

pip install -r requirements.txt

---

### 3. Database Setup

Run migrations:

python manage.py makemigrations

python manage.py migrate

Create admin user:

python manage.py createsuperuser

---

### 4. Run the Application

python manage.py runserver

Open in browser:

Main: http://127.0.0.1:8000  
Admin panel: http://127.0.0.1:8000/admin

---

## 🧑‍🏫 Usage

1. Login to the admin panel  
2. Create:
   - Students  
   - Classes  
   - Sessions  
3. Mark attendance for each session  
4. Monitor absence records

---

## 📁 Project Structure

attendance/     – main application logic  
templates/      – admin custom templates  
upcabsence/     – project configuration  
manage.py       – Django entry point  

---

## ⚠️ Common Issues

Migration error:

python manage.py migrate

Port already in use:

python manage.py runserver 8001

---

## 📜 License

This project is licensed under the MIT License.

---

## 🧑‍💻 Author
**Nadir Azizov**<br>
n.azizov@ufaz.az<br>
nadirabulfazazizov@gmail.com<br>
UFAZ — FEWP Project (2025)<br>

---

This project is free to use for learning and academic purposes.