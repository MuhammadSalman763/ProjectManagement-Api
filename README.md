# Collaborative Project Management API

A professional RESTful backend API for a collaborative project management system built with **Django** and **Django REST Framework**.

The system provides secure APIs for user authentication, project management, task management, document management, comments, timeline events, and notifications.

The API uses **JWT authentication** together with **role-based authorization** to control which users can create, read, update, and delete resources.

---

## Features

### Authentication

* User registration
* JWT login
* JWT access token
* JWT refresh token
* Logout
* Refresh-token blacklisting

### User Profiles

* Profile picture upload
* Contact number
* User roles
* Manager role
* QA role
* Developer role

### Role-Based Authorization

The API supports three roles:

* **Manager**
* **QA**
* **Developer**

Authentication and authorization are handled separately.

A user must first be authenticated with a valid JWT access token. The user's role is then checked before protected operations are allowed.

### Project Management

* Create projects
* List projects
* View project details
* Update projects
* Delete projects

### Task Management

* Create tasks
* List tasks
* View task details
* Update tasks
* Delete tasks
* Assign tasks

### Document Management

* Upload documents
* List documents
* View document details
* Document access based on user permissions

### Collaboration

* Create comments
* List comments
* View comment details
* Update comments
* Delete comments
* View project comments

### Activity

* View timeline events

### Notifications

* View notifications
* Mark notifications as read

### Testing

The project includes automated API tests for:

* Authentication
* Registration
* Login
* Logout
* Project permissions
* Task permissions
* Task assignment permissions
* Document permissions
* Comment permissions
* Timeline permissions
* Notification permissions
* Unauthorized access
* Forbidden role access
* Resource ownership checks

---

# Technology Stack

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python                | Programming language            |
| Django                | Backend framework               |
| Django REST Framework | REST API                        |
| Simple JWT            | JWT authentication              |
| DRF Spectacular       | OpenAPI / Swagger documentation |
| SQLite                | Development database            |
| Pillow                | Image processing                |
| python-dotenv         | Environment variables           |
| Git                   | Version control                 |
| GitHub                | Repository hosting              |
| Postman               | API testing                     |

---

# Project Structure

```text
ProjectManagement-Api/

├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── project_management/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── media/
│   └── profile_pictures/
│
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── API_DOCUMENTATION.md
```

---

# Requirements

Before running the project, install:

* Python 3.x
* Git
* pip
* Virtual environment
* Postman (recommended)

Check Python:

```bash
python --version
```

Check Git:

```bash
git --version
```

Check pip:

```bash
pip --version
```

---

# Installation and Setup

## 1. Clone Repository

```bash
git clone https://github.com/MuhammadSalman763/ProjectManagement-Api.git
```

Move into the project directory:

```bash
cd ProjectManagement-Api
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

### Windows CMD

```bash
venv\Scripts\activate
```

### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

### Git Bash

```bash
source venv/Scripts/activate
```

After activation:

```text
(venv)
```

should appear in the terminal.

---

## 3. Install Dependencies

Install all project dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is unavailable, install the main packages:

```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install drf-spectacular
pip install pillow
pip install python-dotenv
```

Generate the requirements file:

```bash
pip freeze > requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

JWT_ACCESS_LIFETIME=5
JWT_REFRESH_LIFETIME=1

TIME_ZONE=Asia/Karachi
```

Do not commit `.env` to GitHub.

Recommended `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
db.sqlite3
media/
```

---

# Database Setup

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

---

# Create Superuser

Create an administrative user:

```bash
python manage.py createsuperuser
```

Enter the requested:

```text
Username
Email
Password
Password confirmation
```

---

# Check Django Configuration

Run:

```bash
python manage.py check
```

Expected:

```text
System check identified no issues
```

---

# Run Development Server

Start the development server:

```bash
python manage.py runserver
```

The application will normally be available at:

```text
http://127.0.0.1:8000/
```

---

# Django Admin

Open:

```text
http://127.0.0.1:8000/admin/
```

Login using the superuser credentials.

---

# API Documentation

Detailed API documentation is maintained separately in:

```text
API_DOCUMENTATION.md
```

Swagger UI:

```text
http://127.0.0.1:8000/api/docs/
```

ReDoc:

```text
http://127.0.0.1:8000/api/redoc/
```

OpenAPI schema:

```text
http://127.0.0.1:8000/api/schema/
```

---

# Authentication

The API uses JWT authentication.

After successful login, the API returns:

```json
{
    "refresh": "REFRESH_TOKEN",
    "access": "ACCESS_TOKEN"
}
```

Use the access token when calling protected endpoints:

```http
Authorization: Bearer ACCESS_TOKEN
```

---

# Role-Based Authorization

The application uses three roles.

## Manager

Managers have the highest level of access.

They can:

* Create projects
* View projects
* Update projects
* Delete projects
* Create tasks
* View tasks
* Update tasks
* Delete tasks
* Assign tasks
* Upload documents
* View documents
* Manage comments
* View timeline events
* View notifications
* Mark notifications as read

## QA

QA users can:

* View projects
* View tasks
* Update tasks
* Upload documents
* View documents
* Create comments
* View comments
* Update/delete their own comments
* View timeline events
* View notifications
* Mark their notifications as read

QA users cannot:

* Create projects
* Delete projects
* Assign tasks
* Delete other users' comments

## Developer

Developers can:

* View projects
* View tasks
* Update tasks assigned to them
* Upload documents
* View documents
* Create comments
* View comments
* Update/delete their own comments
* View timeline events
* View notifications
* Mark their notifications as read

Developers cannot:

* Create projects
* Update/delete projects
* Delete tasks
* Assign tasks
* Modify other users' comments

---

# Permission Summary

| Resource / Action          | Manager |  QA |        Developer |
| -------------------------- | ------: | --: | ---------------: |
| Create Project             |     Yes |  No |               No |
| View Project               |     Yes | Yes |              Yes |
| Update Project             |     Yes |  No |               No |
| Delete Project             |     Yes |  No |               No |
| Create Task                |     Yes |  No |               No |
| View Task                  |     Yes | Yes |              Yes |
| Update Task                |     Yes | Yes | Assigned/Allowed |
| Delete Task                |     Yes |  No |               No |
| Assign Task                |     Yes |  No |               No |
| Upload Document            |     Yes | Yes |              Yes |
| View Document              |     Yes | Yes |              Yes |
| Create Comment             |     Yes | Yes |              Yes |
| View Comment               |     Yes | Yes |              Yes |
| Update Own Comment         |     Yes | Yes |              Yes |
| Delete Own Comment         |     Yes | Yes |              Yes |
| Update Other Comment       |     Yes |  No |               No |
| Delete Other Comment       |     Yes |  No |               No |
| View Timeline              |     Yes | Yes |              Yes |
| View Notifications         |     Yes | Yes |              Yes |
| Mark Own Notification Read |     Yes | Yes |              Yes |

---

# API Testing with Postman

## Register

```http
POST http://127.0.0.1:8000/api/register/
```

Use:

```text
Body → form-data
```

Example:

```text
username = salman767
email = salman@example.com
password = Salman12345
password2 = Salman12345
role = developer
contact_number = 3001234567
profile_picture = profile.jpg
```

---

## Login

```http
POST http://127.0.0.1:8000/api/login/
```

Example:

```json
{
    "username": "salman767",
    "password": "Salman12345"
}
```

Copy the returned access token.

---

## Configure Authorization

For protected endpoints:

```text
Authorization → Bearer Token
```

Paste:

```text
ACCESS_TOKEN
```

---

# Testing Role-Based Authorization

Test the same endpoint with different user roles.

For example:

### Manager

```text
POST /api/projects/
```

Expected:

```text
201 Created
```

### QA

```text
POST /api/projects/
```

Expected:

```text
403 Forbidden
```

### Developer

```text
POST /api/projects/
```

Expected:

```text
403 Forbidden
```

This verifies that authentication alone is not enough and role-based authorization is enforced.

---

# Automated Testing

Run all tests:

```bash
python manage.py test
```

Run accounts tests:

```bash
python manage.py test accounts
```

Run with detailed output:

```bash
python manage.py test accounts -v 2
```

Expected:

```text
Found X test(s).

System check identified no issues.

...

OK
```

---

# Authorization Test Cases

The automated test suite should verify:

### Authentication

* Registration succeeds
* Duplicate username is rejected
* Invalid password is rejected
* Login succeeds
* Invalid login is rejected
* Logout succeeds
* Invalid refresh token is rejected

### Project Authorization

* Manager can create projects
* QA cannot create projects
* Developer cannot create projects
* Manager can update projects
* QA cannot update projects
* Developer cannot update projects
* Manager can delete projects
* QA cannot delete projects
* Developer cannot delete projects
* Authenticated users can view projects

### Task Authorization

* Manager can create tasks
* QA cannot create tasks
* Developer cannot create tasks
* Manager can update tasks
* QA can update allowed tasks
* Developer can update assigned tasks
* Unauthorized users cannot update tasks
* Manager can delete tasks
* QA cannot delete tasks
* Developer cannot delete tasks
* Manager can assign tasks
* QA cannot assign tasks
* Developer cannot assign tasks

### Document Authorization

* Manager can upload documents
* QA can upload documents
* Developer can upload documents
* Authenticated users can view documents
* Unauthenticated users cannot access documents

### Comment Authorization

* Authenticated users can create comments
* Users can view comments
* Users can update their own comments
* Users can delete their own comments
* Users cannot update another user's comment
* Users cannot delete another user's comment
* Manager can manage comments

### Timeline Authorization

* Authenticated users can view timeline events
* Unauthenticated users receive `401 Unauthorized`

### Notification Authorization

* Users can view their own notifications
* Users can mark their own notifications as read
* Users cannot modify another user's notifications

### Permission Errors

Verify:

```text
401 Unauthorized
```

for unauthenticated requests.

Verify:

```text
403 Forbidden
```

for authenticated users who do not have the required role.

---

# Media Files

Profile pictures are uploaded using:

```text
multipart/form-data
```

In Postman:

```text
Body
→ form-data
→ profile_picture
→ File
```

Do not send profile pictures as raw JSON.

Make sure Django has:

```text
MEDIA_URL
MEDIA_ROOT
```

configured correctly.

---

# Git Workflow

Check status:

```bash
git status
```

Add changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "feat: add role based authorization"
```

Push changes:

```bash
git push origin main
```

---

# Recommended Commit Structure

Use separate commits for logical changes:

```text
feat: add role based permission classes

feat: apply role permissions to project APIs

feat: apply role permissions to task APIs

feat: apply role permissions to document APIs

feat: apply role permissions to comment APIs

feat: apply role permissions to timeline APIs

feat: apply role permissions to notification APIs

test: add role based authorization test cases

docs: update API documentation

docs: update README with installation and authorization
```

---

# Troubleshooting

## Migration Error

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Server Error

Run:

```bash
python manage.py check
```

Then:

```bash
python manage.py runserver
```

## Authentication Error

If you receive:

```text
Authentication credentials were not provided.
```

send:

```http
Authorization: Bearer ACCESS_TOKEN
```

## Permission Error

If you receive:

```text
403 Forbidden
```

the user is authenticated but does not have the required role or ownership permission.

Check the user's profile role:

```text
manager
qa
developer
```

## Token Expired

Login again:

```http
POST /api/login/
```

and obtain a new access token.

---

# Security

Recommended security practices:

* Set `DEBUG=False` in production.
* Never commit `.env`.
* Use a strong Django `SECRET_KEY`.
* Use HTTPS in production.
* Use secure database credentials.
* Protect JWT secrets.
* Validate uploaded files.
* Restrict sensitive operations using permissions.
* Do not expose private information in API responses.
* Apply ownership checks where required.

---

# Production Deployment

Before deployment:

```bash
python manage.py check --deploy
```

Set:

```env
DEBUG=False
```

Configure:

* Production database
* Allowed hosts
* CORS
* HTTPS
* Static files
* Media files
* Environment variables
* Secret keys

Collect static files:

```bash
python manage.py collectstatic
```

---

# Development Workflow

```text
1. Clone repository
       ↓
2. Create virtual environment
       ↓
3. Activate virtual environment
       ↓
4. Install requirements
       ↓
5. Configure .env
       ↓
6. Run migrations
       ↓
7. Create superuser
       ↓
8. Start server
       ↓
9. Open Swagger
       ↓
10. Register user
       ↓
11. Assign/select user role
       ↓
12. Login
       ↓
13. Copy JWT access token
       ↓
14. Authorize protected APIs
       ↓
15. Test APIs according to user role
       ↓
16. Run automated tests
```

---

# Project Status

The project provides a Django REST Framework backend for collaborative project management with:

* JWT authentication
* Role-based authorization
* Project management
* Task management
* Task assignment
* Document management
* Comments
* Timeline events
* Notifications
* Automated API tests
* Swagger/OpenAPI documentation

---

# Author

**Muhammad Salman**

GitHub:

https://github.com/MuhammadSalman763

Repository:

https://github.com/MuhammadSalman763/ProjectManagement-Api

---

# License
