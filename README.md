# Project Management API

A RESTful backend API for a collaborative Project Management application built with **Django**, **Django REST Framework (DRF)**, **JWT Authentication**, and **drf-spectacular**.

The API provides user authentication, project management, task management, document management, comments, timeline events, and notifications.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Features](#features)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Requirements](#requirements)
* [Installation and Setup](#installation-and-setup)
* [Environment Variables](#environment-variables)
* [Database Setup](#database-setup)
* [Create Superuser](#create-superuser)
* [Run Development Server](#run-development-server)
* [API Documentation](#api-documentation)
* [Authentication](#authentication)
* [User Authentication APIs](#1-user-authentication-apis)
* [Project APIs](#2-project-apis)
* [Task APIs](#3-task-apis)
* [Document APIs](#4-document-apis)
* [Comment APIs](#5-comment-apis)
* [Timeline APIs](#6-timeline-event-apis)
* [Notification APIs](#7-notification-apis)
* [HTTP Status Codes](#http-status-codes)
* [Testing](#testing)
* [Git Workflow](#git-workflow)
* [Troubleshooting](#troubleshooting)
* [Future Improvements](#future-improvements)

---

# Project Overview

The Project Management API is designed for collaborative teams where users can:

* Register an account
* Login using JWT authentication
* Logout and blacklist refresh tokens
* Create projects
* View projects
* Update projects
* Delete projects
* Create tasks
* View tasks
* View task details
* Update tasks
* Delete tasks
* Assign tasks
* Upload documents
* View documents
* View document details
* Create comments
* View comments
* Update comments
* Delete comments
* View project comments
* View timeline events
* View notifications
* Mark notifications as read

---

# Features

## Authentication

* User registration
* JWT login
* Access token
* Refresh token
* JWT logout
* Refresh token blacklisting

## User Profile

* Profile picture upload
* User role
* Contact number
* Manager
* QA
* Developer

## Project Management

* Create projects
* List projects
* Project details
* Update projects
* Delete projects

## Task Management

* Create tasks
* List tasks
* Task details
* Update tasks
* Delete tasks
* Assign tasks

## Document Management

* Upload documents
* List documents
* Document details

## Collaboration

* Create comments
* List comments
* Update comments
* Delete comments
* Project comments

## Activity and Notifications

* Timeline events
* User notifications
* Mark notifications as read

---

# Technology Stack

| Technology            | Purpose                       |
| --------------------- | ----------------------------- |
| Python                | Programming language          |
| Django                | Backend framework             |
| Django REST Framework | REST APIs                     |
| Simple JWT            | JWT authentication            |
| DRF Spectacular       | Swagger/OpenAPI documentation |
| SQLite / Database     | Data storage                  |
| Pillow                | Image processing              |
| Git                   | Version control               |
| GitHub                | Repository hosting            |
| Postman               | API testing                   |

---

# Project Structure

```text
ProjectManagement-Api/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
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
└── README.md
```

---

# Requirements

Before installing the project, make sure the following software is installed:

* Python 3.x
* Git
* pip
* Virtual Environment
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

## Step 1 — Clone the Repository

Clone the GitHub repository:

```bash
git clone https://github.com/MuhammadSalman763/ProjectManagement-Api.git
```

Move into the project directory:

```bash
cd ProjectManagement-Api
```

---

## Step 2 — Create Virtual Environment

Create a virtual environment:

### Windows

```bash
python -m venv venv
```

Activate it:

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

After activation, the terminal should show:

```text
(venv)
```

---

# Step 3 — Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, install the main dependencies:

```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install drf-spectacular
pip install pillow
python-dotenv
```

Then generate requirements:

```bash
pip freeze > requirements.txt
```

---

# Step 4 — Configure Environment Variables

Create a `.env` file in the root directory.

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

### Important

Do not commit `.env` to GitHub.

Add it to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
db.sqlite3
media/
```

---

# Step 5 — Run Migrations

Run:

```bash
python manage.py makemigrations
```

Then:

```bash
python manage.py migrate
```

---

# Step 6 — Create Superuser

Create an admin user:

```bash
python manage.py createsuperuser
```

Enter:

```text
Username:
Email:
Password:
Password confirmation:
```

---

# Step 7 — Run the Server

Start Django:

```bash
python manage.py runserver
```

The API will normally be available at:

```text
http://127.0.0.1:8000/
```

---

# Step 8 — Open Django Admin

Open:

```text
http://127.0.0.1:8000/admin/
```

Login using your superuser credentials.

---

# API Documentation

The project uses **drf-spectacular** for automatic OpenAPI documentation.

Swagger UI:

```text
/api/docs/
```

ReDoc:

```text
/api/redoc/
```

OpenAPI schema:

```text
/api/schema/
```

Swagger is recommended because it allows developers to test APIs directly from the browser.

---

# Base URL

For local development:

```text
http://127.0.0.1:8000
```

All API endpoints are based on this URL.

Example:

```text
http://127.0.0.1:8000/api/login/
```

---

# Authentication

Most APIs require JWT authentication.

After successful login, the API returns:

```json
{
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN"
}
```

Use the access token in protected requests.

Header:

```http
Authorization: Bearer ACCESS_TOKEN
```

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

---

# 1. User Authentication APIs

---

## 1.1 Register User

### Endpoint

```http
POST /api/register/
```

### Authentication

Not required.

### Required Permissions

Public.

### Content Type

Because profile picture can be uploaded:

```text
multipart/form-data
```

### Required Fields

```text
username
email
password
password2
```

Profile information may include:

```text
profile_picture
role
contact_number
```

### Example Request

```text
username = salman767
email = salman@example.com
password = Salman12345
password2 = Salman12345
role = developer
contact_number = 3001234567
profile_picture = profile.jpg
```

### Success Response

```json
{
    "message": "User registered successfully",
    "user": {
        "username": "salman767",
        "email": "salman@example.com"
    }
}
```

### Error Responses

Invalid password:

```json
{
    "password": [
        "Passwords do not match."
    ]
}
```

Duplicate username:

```json
{
    "username": [
        "A user with that username already exists."
    ]
}
```

Missing required field:

```json
{
    "email": [
        "This field is required."
    ]
}
```

### Status Codes

```text
201 Created
400 Bad Request
```

---

# 1.2 Login

### Endpoint

```http
POST /api/login/
```

### Authentication

Not required.

### Required Permissions

Public.

### Request Body

```json
{
    "username": "salman767",
    "password": "Salman12345"
}
```

### Success Response

```json
{
    "refresh": "REFRESH_TOKEN",
    "access": "ACCESS_TOKEN"
}
```

### Error Response

```json
{
    "detail": "Invalid username or password."
}
```

### Status Codes

```text
200 OK
401 Unauthorized
```

---

# 1.3 Logout

### Endpoint

```http
POST /api/logout/
```

### Authentication

Required.

### Required Permissions

Authenticated user.

### Request Body

```json
{
    "refresh": "REFRESH_TOKEN"
}
```

### Headers

```http
Authorization: Bearer ACCESS_TOKEN
```

### Success Response

```json
{
    "message": "Logout successful"
}
```

### Error Response

```json
{
    "detail": "Invalid token"
}
```

### Status Codes

```text
200 OK
400 Bad Request
401 Unauthorized
```

---

# 2. Project APIs

---

# 2.1 Create Project

### Endpoint

```http
POST /api/projects/
```

### Authentication

Required.

### Permission

Authenticated users.

### Headers

```http
Authorization: Bearer ACCESS_TOKEN
Content-Type: application/json
```

### Example Request

```json
{
    "name": "Project Management System",
    "description": "Collaborative project management application"
}
```

### Success Response

```json
{
    "id": 1,
    "name": "Project Management System",
    "description": "Collaborative project management application"
}
```

### Error Response

```json
{
    "name": [
        "This field is required."
    ]
}
```

### Status Codes

```text
201 Created
400 Bad Request
401 Unauthorized
```

---

# 2.2 List Projects

### Endpoint

```http
GET /api/projects/list/
```

### Authentication

Required.

### Permission

Authenticated users.

### Request Parameters

None required.

### Example Request

```http
GET /api/projects/list/
```

### Success Response

```json
[
    {
        "id": 1,
        "name": "Project Management System",
        "description": "Collaborative project management application"
    },
    {
        "id": 2,
        "name": "Student Management System",
        "description": "Student management API"
    }
]
```

### Error Response

```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Status Codes

```text
200 OK
401 Unauthorized
```

---

# 2.3 Project Detail

### Endpoint

```http
GET /api/projects/{id}/
```

### Authentication

Required.

### Permission

Authenticated users.

### Path Parameter

```text
id
```

Example:

```http
GET /api/projects/1/
```

### Success Response

```json
{
    "id": 1,
    "name": "Project Management System",
    "description": "Collaborative project management application"
}
```

### Error Response

```json
{
    "detail": "Not found."
}
```

### Status Codes

```text
200 OK
404 Not Found
401 Unauthorized
```

---

# 2.4 Update Project

### Endpoint

```http
PUT /api/projects/{id}/update/
```

or use the supported partial update behavior if configured.

### Authentication

Required.

### Permission

Authenticated user with permission to modify the project.

### Example Request

```http
PUT /api/projects/1/update/
```

```json
{
    "name": "Updated Project Name",
    "description": "Updated project description"
}
```

### Success Response

```json
{
    "id": 1,
    "name": "Updated Project Name",
    "description": "Updated project description"
}
```

### Error Response

```json
{
    "detail": "Not found."
}
```

### Status Codes

```text
200 OK
400 Bad Request
401 Unauthorized
404 Not Found
```

---

# 2.5 Delete Project

### Endpoint

```http
DELETE /api/projects/{id}/delete/
```

### Authentication

Required.

### Permission

Authenticated user with permission to delete the project.

### Example

```http
DELETE /api/projects/1/delete/
```

### Success Response

```json
{
    "message": "Project deleted successfully"
}
```

### Error Response

```json
{
    "detail": "Not found."
}
```

### Status Codes

```text
204 No Content / 200 OK
401 Unauthorized
404 Not Found
```

---

# 3. Task APIs

---

# 3.1 Create Task

### Endpoint

```http
POST /api/tasks/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example Request

```json
{
    "title": "Create Login API",
    "description": "Implement JWT login functionality",
    "project": 1
}
```

### Success Response

```json
{
    "id": 1,
    "title": "Create Login API",
    "description": "Implement JWT login functionality",
    "project": 1
}
```

### Error Responses

```json
{
    "title": [
        "This field is required."
    ]
}
```

```json
{
    "project": [
        "Invalid pk."
    ]
}
```

### Status Codes

```text
201 Created
400 Bad Request
401 Unauthorized
```

---

# 3.2 List Tasks

### Endpoint

```http
GET /api/tasks/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example Request

```http
GET /api/tasks/
```

### Success Response

```json
[
    {
        "id": 1,
        "title": "Create Login API",
        "description": "Implement JWT login functionality",
        "project": 1
    }
]
```

### Status Codes

```text
200 OK
401 Unauthorized
```

---

# 3.3 Task Detail

### Endpoint

```http
GET /api/tasks/{id}/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example

```http
GET /api/tasks/1/
```

### Success Response

```json
{
    "id": 1,
    "title": "Create Login API",
    "description": "Implement JWT login functionality",
    "project": 1
}
```

### Error Response

```json
{
    "detail": "Not found."
}
```

### Status Codes

```text
200 OK
401 Unauthorized
404 Not Found
```

---

# 3.4 Update Task

### Endpoint

```http
PUT /api/tasks/{id}/update/
```

### Authentication

Required.

### Permission

Authenticated user with update permission.

### Example Request

```json
{
    "title": "Updated Login API",
    "description": "Updated task description"
}
```

### Success Response

```json
{
    "id": 1,
    "title": "Updated Login API",
    "description": "Updated task description"
}
```

### Status Codes

```text
200 OK
400 Bad Request
401 Unauthorized
404 Not Found
```

---

# 3.5 Delete Task

### Endpoint

```http
DELETE /api/tasks/{id}/delete/
```

### Authentication

Required.

### Permission

Authenticated user with delete permission.

### Example

```http
DELETE /api/tasks/1/delete/
```

### Success Response

```json
{
    "message": "Task deleted successfully"
}
```

### Status Codes

```text
200 OK / 204 No Content
401 Unauthorized
404 Not Found
```

---

# 3.6 Assign Task

### Endpoint

```http
POST /api/tasks/{id}/assign/
```

### Authentication

Required.

### Permission

Authenticated user with task assignment permission.

### Example Request

```json
{
    "assigned_to": 2
}
```

### Success Response

```json
{
    "message": "Task assigned successfully"
}
```

### Error Response

```json
{
    "assigned_to": [
        "Invalid user."
    ]
}
```

### Status Codes

```text
200 OK
400 Bad Request
401 Unauthorized
404 Not Found
```

---

# 4. Document APIs

---

# 4.1 Upload Document

### Endpoint

```http
POST /api/documents/
```

### Authentication

Required.

### Permission

Authenticated users.

### Content Type

```text
multipart/form-data
```

### Example Request

```text
title = Project Documentation
project = 1
file = documentation.pdf
```

### Success Response

```json
{
    "id": 1,
    "title": "Project Documentation",
    "project": 1,
    "file": "/media/documents/documentation.pdf"
}
```

### Error Response

```json
{
    "file": [
        "This field is required."
    ]
}
```

### Status Codes

```text
201 Created
400 Bad Request
401 Unauthorized
```

---

# 4.2 List Documents

### Endpoint

```http
GET /api/documents/list/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example

```http
GET /api/documents/list/
```

### Success Response

```json
[
    {
        "id": 1,
        "title": "Project Documentation",
        "project": 1,
        "file": "/media/documents/documentation.pdf"
    }
]
```

### Status Codes

```text
200 OK
401 Unauthorized
```

---

# 4.3 Document Detail

### Endpoint

```http
GET /api/documents/{id}/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example

```http
GET /api/documents/1/
```

### Success Response

```json
{
    "id": 1,
    "title": "Project Documentation",
    "project": 1,
    "file": "/media/documents/documentation.pdf"
}
```

### Error Response

```json
{
    "detail": "Not found."
}
```

### Status Codes

```text
200 OK
401 Unauthorized
404 Not Found
```

---

# 5. Comment APIs

---

# 5.1 Create Comment

### Endpoint

```http
POST /api/comments/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example Request

```json
{
    "project": 1,
    "content": "This project is progressing well."
}
```

### Success Response

```json
{
    "id": 1,
    "project": 1,
    "content": "This project is progressing well."
}
```

### Error Response

```json
{
    "content": [
        "This field is required."
    ]
}
```

### Status Codes

```text
201 Created
400 Bad Request
401 Unauthorized
```

---

# 5.2 List Comments

### Endpoint

```http
GET /api/comments/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example

```http
GET /api/comments/
```

### Success Response

```json
[
    {
        "id": 1,
        "project": 1,
        "content": "This project is progressing well."
    }
]
```

### Status Codes

```text
200 OK
401 Unauthorized
```

---

# 5.3 Comment Detail

### Endpoint

```http
GET /api/comments/{id}/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example

```http
GET /api/comments/1/
```

### Success Response

```json
{
    "id": 1,
    "project": 1,
    "content": "This project is progressing well."
}
```

### Error Response

```json
{
    "detail": "Not found."
}
```

---

# 5.4 Update Comment

### Endpoint

```http
PUT /api/comments/{id}/
```

### Authentication

Required.

### Permission

Comment author / authorized authenticated user.

### Example Request

```json
{
    "content": "Updated project comment."
}
```

### Success Response

```json
{
    "id": 1,
    "content": "Updated project comment."
}
```

### Status Codes

```text
200 OK
400 Bad Request
401 Unauthorized
404 Not Found
```

---

# 5.5 Delete Comment

### Endpoint

```http
DELETE /api/comments/{id}/
```

### Authentication

Required.

### Permission

Comment author / authorized authenticated user.

### Example

```http
DELETE /api/comments/1/
```

### Success Response

```json
{
    "message": "Comment deleted successfully"
}
```

### Status Codes

```text
200 OK / 204 No Content
401 Unauthorized
404 Not Found
```

---

# 5.6 Project Comments

### Endpoint

```http
GET /api/projects/{id}/comments/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example

```http
GET /api/projects/1/comments/
```

### Success Response

```json
[
    {
        "id": 1,
        "project": 1,
        "content": "This project is progressing well."
    }
]
```

### Error Response

```json
{
    "detail": "Not found."
}
```

### Status Codes

```text
200 OK
401 Unauthorized
404 Not Found
```

---

# 6. Timeline Event APIs

---

# 6.1 List Timeline Events

### Endpoint

```http
GET /api/timeline/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example

```http
GET /api/timeline/
```

### Success Response

```json
[
    {
        "id": 1,
        "event_type": "project_created",
        "description": "Project was created",
        "created_at": "2026-08-25T10:30:00Z"
    }
]
```

### Status Codes

```text
200 OK
401 Unauthorized
```

---

# 7. Notification APIs

---

# 7.1 List Notifications

### Endpoint

```http
GET /api/notifications/
```

### Authentication

Required.

### Permission

Authenticated users.

### Example

```http
GET /api/notifications/
```

### Success Response

```json
[
    {
        "id": 1,
        "message": "You have been assigned a task.",
        "is_read": false
    }
]
```

### Status Codes

```text
200 OK
401 Unauthorized
```

---

# 7.2 Mark Notification as Read

### Endpoint

```http
PATCH /api/notifications/{id}/read/
```

### Authentication

Required.

### Permission

Authenticated owner of the notification.

### Example

```http
PATCH /api/notifications/1/read/
```

### Success Response

```json
{
    "message": "Notification marked as read"
}
```

### Error Response

```json
{
    "detail": "Not found."
}
```

### Status Codes

```text
200 OK
401 Unauthorized
404 Not Found
```

---

# API Summary

| #  | API                    | Method | Authentication |
| -- | ---------------------- | ------ | -------------- |
| 1  | Register               | POST   | No             |
| 2  | Login                  | POST   | No             |
| 3  | Logout                 | POST   | Yes            |
| 4  | Create Project         | POST   | Yes            |
| 5  | List Projects          | GET    | Yes            |
| 6  | Project Detail         | GET    | Yes            |
| 7  | Update Project         | PUT    | Yes            |
| 8  | Delete Project         | DELETE | Yes            |
| 9  | Create Task            | POST   | Yes            |
| 10 | List Tasks             | GET    | Yes            |
| 11 | Task Detail            | GET    | Yes            |
| 12 | Update Task            | PUT    | Yes            |
| 13 | Delete Task            | DELETE | Yes            |
| 14 | Assign Task            | POST   | Yes            |
| 15 | Upload Document        | POST   | Yes            |
| 16 | List Documents         | GET    | Yes            |
| 17 | Document Detail        | GET    | Yes            |
| 18 | Create Comment         | POST   | Yes            |
| 19 | List Comments          | GET    | Yes            |
| 20 | Comment Detail         | GET    | Yes            |
| 21 | Update Comment         | PUT    | Yes            |
| 22 | Delete Comment         | DELETE | Yes            |
| 23 | Project Comments       | GET    | Yes            |
| 24 | Timeline Events        | GET    | Yes            |
| 25 | Notifications          | GET    | Yes            |
| 26 | Mark Notification Read | PATCH  | Yes            |

---

# HTTP Status Codes

| Status Code | Meaning                                       |
| ----------- | --------------------------------------------- |
| 200         | Request successful                            |
| 201         | Resource created                              |
| 204         | Resource deleted successfully                 |
| 400         | Bad Request                                   |
| 401         | Authentication required / invalid credentials |
| 403         | Permission denied                             |
| 404         | Resource not found                            |
| 405         | Method not allowed                            |
| 500         | Internal server error                         |

---

# Testing

The project contains automated tests.

Run all tests:

```bash
python manage.py test
```

Run only the accounts application:

```bash
python manage.py test accounts
```

Run with verbosity:

```bash
python manage.py test accounts -v 2
```

Expected output:

```text
Found X test(s).
System check identified no issues.
...
OK
```

---

# Testing APIs Using Postman

## Step 1 — Register

```http
POST http://127.0.0.1:8000/api/register/
```

Use:

```text
Body → form-data
```

Add required registration fields.

---

## Step 2 — Login

```http
POST http://127.0.0.1:8000/api/login/
```

Body:

```json
{
    "username": "salman767",
    "password": "Salman12345"
}
```

Copy the returned access token.

---

## Step 3 — Set Authorization

For protected APIs:

```text
Authorization
Bearer Token
```

Paste:

```text
ACCESS_TOKEN
```

---

## Step 4 — Test Project APIs

Example:

```http
POST http://127.0.0.1:8000/api/projects/
```

Body:

```json
{
    "name": "Test Project",
    "description": "Testing project API"
}
```

Then test:

```http
GET /api/projects/list/
```

```http
GET /api/projects/1/
```

```http
PUT /api/projects/1/update/
```

```http
DELETE /api/projects/1/delete/
```

---

# Swagger API Testing

After starting the server, open:

```text
http://127.0.0.1:8000/api/docs/
```

Swagger provides:

* All API endpoints
* HTTP methods
* Request parameters
* Request body
* Response schemas
* Authentication
* Interactive API testing

For protected APIs, authorize Swagger with:

```text
Bearer ACCESS_TOKEN
```

---

# Environment Configuration

Production deployment should use:

```env
DEBUG=False
```

A secure `SECRET_KEY` must be generated for production.

Never expose:

* SECRET_KEY
* Database passwords
* JWT secrets
* API keys
* `.env`

in the public GitHub repository.

---

# Git Workflow

Check repository status:

```bash
git status
```

Add files:

```bash
git add .
```

Create a commit:

```bash
git commit -m "Add project management API documentation"
```

Push changes:

```bash
git push origin main
```

---

# Recommended Commit Structure

For ticket-based development, use separate commits.

Example:

```text
feat: implement user registration API
feat: implement JWT login API
feat: implement logout API
feat: implement project creation API
feat: implement project listing API
feat: implement project detail API
feat: implement project update API
feat: implement project deletion API
feat: implement task creation API
feat: implement task listing API
feat: implement task detail API
feat: implement task update API
feat: implement task deletion API
feat: implement task assignment API
feat: implement document upload API
feat: implement document listing API
feat: implement document detail API
feat: implement comment APIs
feat: implement timeline event API
feat: implement notification API
test: add API test cases
docs: add complete API documentation
```

---

# Troubleshooting

## Migration Error

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Server Not Starting

Check:

```bash
python manage.py check
```

Then:

```bash
python manage.py runserver
```

---

## Authentication Error

If you receive:

```text
Authentication credentials were not provided.
```

Make sure the request contains:

```http
Authorization: Bearer ACCESS_TOKEN
```

---

## Token Expired

Login again and obtain a new access token.

```http
POST /api/login/
```

---

## Media File Not Showing

Make sure `MEDIA_URL` and `MEDIA_ROOT` are configured and that the development URL configuration serves media files.

---

## Profile Picture Upload

Use Postman:

```text
Body
→ form-data
```

Set:

```text
profile_picture = File
```

Do not send the image field as raw JSON.

---

# Security

The following security practices are recommended:

* Keep `DEBUG=False` in production.
* Never commit `.env`.
* Use a strong Django secret key.
* Use HTTPS in production.
* Use secure database credentials.
* Rotate JWT secrets when required.
* Validate uploaded files.
* Restrict permissions for sensitive operations.
* Do not expose private information in API responses.

---

# Production Deployment

Before deploying:

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

Then collect static files:

```bash
python manage.py collectstatic
```

---

# API Development Workflow

A new developer can follow this workflow:

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
11. Login
        ↓
12. Copy JWT access token
        ↓
13. Authorize protected APIs
        ↓
14. Test Project APIs
        ↓
15. Test Task APIs
        ↓
16. Test Document APIs
        ↓
17. Test Comment APIs
        ↓
18. Test Timeline APIs
        ↓
19. Test Notification APIs
        ↓
20. Run automated tests
```

---

# Complete API Flow

A typical user flow is:

```text
Register
   ↓
Login
   ↓
Receive Access + Refresh Token
   ↓
Create Project
   ↓
Create Task
   ↓
Assign Task
   ↓
Upload Document
   ↓
Add Comment
   ↓
View Timeline
   ↓
Receive Notification
   ↓
Mark Notification as Read
   ↓
Logout
```

---

# Project Status

The project implements the backend APIs required for a collaborative project management system using Django REST Framework and JWT authentication.

---

# Author

**Muhammad Salman**

GitHub:

```text
https://github.com/MuhammadSalman763
```

Repository:

```text
https://github.com/MuhammadSalman763/ProjectManagement-Api
```

---

# License

This project is developed for educational and project development purposes.
