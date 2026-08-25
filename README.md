# Collaborative Project Management API

A professional RESTful backend API for a collaborative project management system built with Django and Django REST Framework.

The system provides secure APIs for user authentication, project management, task management, document management, comments, timeline events, and notifications.

The API uses JWT authentication together with role-based authorization to control what each user role can create, read, update, and delete.

---

## Features

### Authentication
- User registration
- JWT login
- JWT access token
- JWT refresh token
- Logout
- Refresh-token blacklisting

### User Profiles
- Profile picture upload
- User roles
- Contact number
- Manager role
- QA role
- Developer role

### Role-Based Authorization

The system supports three roles:

- Manager
- QA
- Developer

Permissions are enforced at API level.

Users must be authenticated and must have the appropriate role to perform protected operations.

### Project Management
- Create projects
- List projects
- View project details
- Update projects
- Delete projects

### Task Management
- Create tasks
- List tasks
- View task details
- Update tasks
- Delete tasks
- Assign tasks

### Document Management
- Upload documents
- List documents
- View document details
- Document version management

### Collaboration
- Create comments
- List comments
- View comment details
- Update comments
- Delete comments
- View project comments

### Activity
- View timeline events

### Notifications
- View notifications
- Mark notifications as read

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend framework |
| Django REST Framework | REST API |
| Simple JWT | JWT authentication |
| DRF Spectacular | OpenAPI / Swagger documentation |
| SQLite | Development database |
| Pillow | Image processing |
| python-dotenv | Environment variables |
| Git | Version control |
| GitHub | Repository hosting |
| Postman | API testing |

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