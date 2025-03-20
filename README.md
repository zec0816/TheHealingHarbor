# The Healing Harbor

## Introduction
With academic pressures, social expectations, and personal responsibilities, mental health issues have largely increased nowadays, especially among university students. However, people may find it difficult to seek help due to stigmas and other concerns. A counseling platform is essential as many people may not have access to them due to geographic location, time constraints, or cost. By providing an accessible and affordable counseling platform, more people may be encouraged to seek help and receive the support they need as the platform can provide resources and guidance to help individuals manage their mental health and reduce their mental strain.

---

## Features
### Students:
- Access Information Section
- Manage Profile: View and Update
- Write Diaries
- Make Appointments
- Review Appointments
- Take the Mental Health Assessment

### Counsellors:
- Manage Information Section: Add, Update and Delete
- Manage Profile: View and Update
- Manage Schedules: Add, Update and Delete
- Review Appointments
- Manage Mental Health Assessment: Add, Update and Delete
- Track Student Assessments’ Progress

### Admin:
- Manage Students and Counsellors: Add, Update and Delete
- Manage Information Section: Add, Update and Delete
- Manage Mental Health Assessment: Add, Update and Delete
- Manage Counsellors’ Schedules: Add, Update and Delete
- Manage Students’ Appointments: Add, Update and Delete

---

## How We Built It
We used an open-source web framework called **Django** to build web applications quickly and efficiently. The programming languages we used are **Python**, along with **HTML, CSS, and JavaScript**. Lastly, we combined our code using **GitHub** and hosted it using **PythonAnywhere**.

---

## Challenges We Ran Into
- Complicated URL routing in Django due to too many webpages
- Getting familiar with GitHub
- Getting more familiar with the Django database
- Uploading profile pictures using the Pillow module
- Setting authentication and authorization for different types of users

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/zec0816/TheHealingHarbor.git
cd TheHealingHarbor
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```sh
pip install django
pip install pillow
```

### 4. Set Up the Database
```sh
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser
```sh
python manage.py createsuperuser
```
Follow the prompts to set up an admin account.

### 6. Run the Development Server
```sh
python manage.py runserver
```
The website will be accessible at `http://127.0.0.1:8000/`.
