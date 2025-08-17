# Car Rental System

A Django-Python based Car Rental System that allows users to rent cars, manage accounts, and view rental history, with an admin interface for fleet management.
---

## 🗂️ Table of Contents

- [🗃️ Project File Structure](#️project-file-structure)
- [⚡ Installation](#installation)
- [🌟 Features](#features)
- [📦 Requirements](#requirements)
- [👤 Roles Within System](#roles-within-system)
  - [🙋‍♂️ Customer (User)](#customer-user)
  - [🛠️ Administrator (Admin)](#administrator-admin)
- [❗ Potential Problems](#potential-problems)
- [🧪 Testing Checklist](#testing)
- [📘 License](#license)
---

## 🗃️ Project File Structure

```bash
car_rental_system/
│
├── base/
│ ├── `__pycache__/`
│ ├── migrations/
│ ├── templates/
│ ├── __init__.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
│
├── car_rental_system/
│ ├── `__pycache__/` 
│ ├── `__init__.py`  
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── rental_management/
│ ├── `__init__.py`
│ └── rental_manager.py
│
├── media/
│ ├── media/
│ └── profile_pics/
│
├── static/
│ ├── images/
│ └── logos/
│
├── templates/
│ ├── main.html
│ └── navbar.html
│
├── venv/
├── db.sqlite3
└── manage.py

---

## Getting Started

```

### ⚡ Installation

1. Open CMD
  - Press
```bash
WIN + R
```
  - Type
```bash
cmd
```

2. Clone the repository (After moving to your desirable directory)
```bash
git clone https://github.com/Usman-Rasheed-Siddiqui/car-rental-system.git
```
  Note: In case you don't have git downloaded, download the zip file of the repository and extract it in your desired folder.
        Then open cmd and follow the following steps.

3. Navigate to the directory
```bash
cd car-rental-system
```

4. Set up virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
```

5. Configure database
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Run requirements.txt
```bash
pip install -r requirements.txt
```

7. Create superuser (for admin access)
```bash
python manage.py createsuperuser
```

8. Run development server
```bash
python manage.py runserver
```

9. Copy this link and paste as URL
  - For page
```bash
http://127.0.0.1:8000/
```
  - For Admin (Django Administration)
```bash
http://127.0.0.1:8000/admin
```
---

## 🌟 Features

- **User Authentication and Profile Management**
  - Create account, login, and update personal details
  - Secure login system with limited login attempts
  - Ability to check user status (e.g., rented car, balance)

- **Car Rental and Return**
  - Rent one car at a time based on availability
  - Return cars with late penalty enforcement
  - Rental receipt generation after each booking

- **Car Fleet Management (Admin)**
  - Add or remove entire car fleets or specific cars
  - View all available cars or specific car details
  - Manage and monitor current reservations

- **Rental History and Feedback**
  - View rental history by user or car
  - Feedback submission by users, accessible by admin

- **Admin Reports and Dashboard**
  - Generate reports for all customers and current rentals
  - Access feedback and rental history summaries

- **Exception Handling System**
  - Custom exceptions for cleaner error messages and safer exits
  - Allows quitting any operation without crashing the system

- **🗃️ Database Management (SQLite)**
    - Models for all entities: Cars, Customers, Rentals
    - Admin dashboard: Built-in Django admin for data management
    - Real-time updates: All changes immediately reflected across the system

- **🌐 Web Interface**
    - User authentication: Login/logout for customers and staff
    - Responsive design: Works on desktop and mobile devices
    - Interactive forms: With validation and error handling

- **📁 File Handling**
    - Car images: Stored in `media/car_images/`
    - Static assets: CSS, JavaScript, logos in `static/`

## 📦 Requirements

- **Prerequisites**
    - Python 3.8+
    - pip
    - pillow
    - django
    - Any other from requirements.txt
---

## 👤 Roles Within System

### 🙋‍♂️ Customer (User)

- Can register a new account and login securely  
- Can rent one car at a time based on availability  
- Can return a rented car (with penalties if late)  
- Can view their rental status (rented car, balance, etc.)  
- Can update personal information (password, address)  
- Can view available cars or search for a specific car  
- Can review their rental history and any car’s history  
- Can provide feedback to the admin  
- Cannot manage or modify the car fleet  

### 🛠️ Administrator (Admin)

- Can login using admin credentials  
- Can add an entire car fleet or individual cars  
- Can remove specific cars or entire fleets  
- Can view all customers and their rental history  
- Can monitor all current rentals and reserved cars  
- Can access user feedback for system improvement  
- Can view all available car IDs and details  
- Can update admin password  
- Cannot rent or reserve cars  
---

## ❗ Potential Problems

### 1. The requirements.txt not running
Open the requirements.txt and install the libraries manually.
```bash
pip install <library_name> 
```

## 🧪 Testing Checklist

Make sure to:

- [ ] Register a new user account and login successfully  
- [ ] Rent an available car and verify receipt generation  
- [ ] Return a car and check if penalties apply for late returns  
- [ ] Attempt login as Admin using admin credentials  
- [ ] Add new cars or remove specific cars via Admin interface  
- [ ] View and verify reports for:  
  - [ ] All customers and their current rentals  
  - [ ] Rental history of specific users and cars  
  - [ ] Currently reserved cars  
- [ ] Submit feedback as a user and access it via Admin panel  
- [ ] Update user balance and personal information  
- [ ] Exit gracefully from any operation to test exception handling  
---


## 📘 License

This project is developed solely for educational use and academic evaluation. It is not intended for commercial deployment or distribution.

---
