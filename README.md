# Meeting Recording System

**DEPLOYED URL:**  
https://attendance-system-soqv.onrender.com

A Django-based web application for managing meetings and attendance at Barangay Larong. Admins can create and manage meetings, while users can view and mark their attendance.

## Prerequisites

- Python 3.8 or higher  
- pip (Python package installer)  
- Git  
- Django  
- (Optional) VS Code or any code editor

## Features

- Separate user roles: Superuser (admin) and regular user
- Admin panel for creating, ending, and managing meetings
- Automatic movement of meetings between Upcoming, Ongoing, and Past sections
- Regular users can mark their attendance
- Admins can view a list of attendees per meeting
- Announcements are shown for upcoming and ongoing meetings
- Secure login using cellphone number and password
- Google Calendar sync integration (optional)
- Clean and responsive HTML template design

## Installation

Clone the repository:

## Create & Activate Virtual Environment

python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

## Install Dependencies

pip install -r requirements.txt

## Apply Migrations

python manage.py migrate

## Create Superuser

python manage.py createsuperuser

## Run Development Server

python manage.py runserver

## LIVE DEPLOYMENT

# Log-in Account:

Username: admin
Password: MyPassword


