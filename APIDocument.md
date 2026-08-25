# Project Management API Documentation

RESTful API documentation for the Collaborative Project Management API.

The API is built using **Django REST Framework**, **JWT Authentication**, **DRF Spectacular**, and **role-based authorization**.

> Installation, virtual environment setup, `.env` configuration, migrations, and server setup are documented in `README.md`.

---

# Table of Contents

* [Base URL](#base-url)
* [Authentication](#authentication)
* [Roles and Authorization](#roles-and-authorization)
* [User Authentication APIs](#1-user-authentication-apis)
* [Project APIs](#2-project-apis)
* [Task APIs](#3-task-apis)
* [Document APIs](#4-document-apis)
* [Comment APIs](#5-comment-apis)
* [Timeline APIs](#6-timeline-apis)
* [Notification APIs](#7-notification-apis)
* [HTTP Status Codes](#http-status-codes)
* [Authorization Rules](#authorization-rules)
* [Testing](#testing)
* [Swagger](#swagger-api-documentation)

---

# Base URL

```text
http://127.0.0.1:8000
```

All API endpoints use this base URL.

Example:

```http
POST /api/login/
```

---

# Authentication

The API uses JWT authentication.

After successful login:

```json
{
    "refresh": "REFRESH_TOKEN",
    "access": "ACCESS_TOKEN"
}
```

Use the access token for protected endpoints:

```http
Authorization: Bearer ACCESS_TOKEN
```

Authentication and authorization are separate:

```text
Authentication
      ↓
Is the user logged in?
      ↓
Authorization
      ↓
Does the user's role allow this action?
```

---

# Roles and Authorization

The API supports:

```text
manager
qa
developer
```

## Manager

Managers have full access to project and task management.

```text
Project: CRUD
Task: CRUD + Assign
Document: CRUD/Access
Comment: Full management
Timeline: Read
Notification: Read + Mark Read
```

## QA

QA users have restricted management access.

```text
Project: Read
Task: Read + Update allowed tasks
Document: Read + Upload
Comment: Create + Read + Own Update/Delete
Timeline: Read
Notification: Read + Own Mark Read
```

## Developer

Developers have restricted project and task access.

```text
Project: Read
Task: Read + Update assigned/allowed tasks
Document: Read + Upload
Comment: Create + Read + Own Update/Delete
Timeline: Read
Notification: Read + Own Mark Read
```

---

# Permission Matrix

| API Operation          | Manager       | QA            | Developer        |
| ---------------------- | ------------- | ------------- | ---------------- |
| Register               | Public        | Public        | Public           |
| Login                  | Public        | Public        | Public           |
| Logout                 | Authenticated | Authenticated | Authenticated    |
| Create Project         | Allow         | Deny          | Deny             |
| List Projects          | Allow         | Allow         | Allow            |
| Project Detail         | Allow         | Allow         | Allow            |
| Update Project         | Allow         | Deny          | Deny             |
| Delete Project         | Allow         | Deny          | Deny             |
| Create Task            | Allow         | Deny          | Deny             |
| List Tasks             | Allow         | Allow         | Allow            |
| Task Detail            | Allow         | Allow         | Allow            |
| Update Task            | Allow         | Allow         | Assigned/Allowed |
| Delete Task            | Allow         | Deny          | Deny             |
| Assign Task            | Allow         | Deny          | Deny             |
| Upload Document        | Allow         | Allow         | Allow            |
| List Documents         | Allow         | Allow         | Allow            |
| Document Detail        | Allow         | Allow         | Allow            |
| Create Comment         | Allow         | Allow         | Allow            |
| List Comments          | Allow         | Allow         | Allow            |
| Comment Detail         | Allow         | Allow         | Allow            |
| Update Own Comment     | Allow         | Allow         | Allow            |
| Delete Own Comment     | Allow         | Allow         | Allow            |
| Update Other Comment   | Allow         | Deny          | Deny             |
| Delete Other Comment   | Allow         | Deny          | Deny             |
| Project Comments       | Allow         | Allow         | Allow            |
| Timeline Events        | Allow         | Allow         | Allow            |
| Notifications          | Own           | Own           | Own              |
| Mark Notification Read | Own           | Own           | Own              |

---

# 1. User Authentication APIs

## 1.1 Register User

### Endpoint

```http
POST /api/register/
```

### Authentication

Not required.

### Permission

Public.

### Content Type

```text
multipart/form-data
```

### Fields

```text
username
email
password
password2
role
contact_number
profile_picture
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

### Success

```json
{
    "message": "User registered successfully",
    "user": {
        "username": "salman767",
        "email": "salman@example.com"
    }
}
```

### Status Codes

```text
201 Created
400 Bad Request
```

---

## 1.2 Login

### Endpoint

```http
POST /api/login/
```

### Authentication

Not required.

### Permission

Public.

### Request

```json
{
    "username": "salman767",
    "password": "Salman12345"
}
```

### Success

```json
{
    "refresh": "REFRESH_TOKEN",
    "access": "ACCESS_TOKEN"
}
```

### Invalid Credentials

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

## 1.3 Logout

### Endpoint

```http
POST /api/logout/
```

### Authentication

Required.

### Permission

Any authenticated user.

### Header

```http
Authorization: Bearer ACCESS_TOKEN
```

### Request

```json
{
    "refresh": "REFRESH_TOKEN"
}
```

### Success

```json
{
    "message": "Logout successful"
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

## 2.1 Create Project

```http
POST /api/projects/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
```

### Denied Roles

```text
QA
Developer
```

### Request

```json
{
    "name": "Project Management System",
    "description": "Collaborative project management application"
}
```

### Success

```json
{
    "id": 1,
    "name": "Project Management System",
    "description": "Collaborative project management application"
}
```

### Permission Denied

```json
{
    "detail": "You do not have permission to perform this action."
}
```

### Status Codes

```text
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
```

---

## 2.2 List Projects

```http
GET /api/projects/list/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Success

```json
[
    {
        "id": 1,
        "name": "Project Management System",
        "description": "Collaborative project management application"
    }
]
```

### Status Codes

```text
200 OK
401 Unauthorized
```

---

## 2.3 Project Detail

```http
GET /api/projects/{id}/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Example

```http
GET /api/projects/1/
```

### Success

```json
{
    "id": 1,
    "name": "Project Management System",
    "description": "Collaborative project management application"
}
```

### Status Codes

```text
200 OK
401 Unauthorized
404 Not Found
```

---

## 2.4 Update Project

```http
PUT /api/projects/{id}/update/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
```

### Denied Roles

```text
QA
Developer
```

### Request

```json
{
    "name": "Updated Project",
    "description": "Updated description"
}
```

### Success

```json
{
    "id": 1,
    "name": "Updated Project",
    "description": "Updated description"
}
```

### Status Codes

```text
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
```

---

## 2.5 Delete Project

```http
DELETE /api/projects/{id}/delete/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
```

### Denied Roles

```text
QA
Developer
```

### Success

```json
{
    "message": "Project deleted successfully"
}
```

### Status Codes

```text
200 OK / 204 No Content
401 Unauthorized
403 Forbidden
404 Not Found
```

---

# 3. Task APIs

## 3.1 Create Task

```http
POST /api/tasks/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
```

### Denied Roles

```text
QA
Developer
```

### Request

```json
{
    "title": "Create Login API",
    "description": "Implement JWT login functionality",
    "project": 1
}
```

### Success

```json
{
    "id": 1,
    "title": "Create Login API",
    "description": "Implement JWT login functionality",
    "project": 1
}
```

### Status Codes

```text
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
```

---

## 3.2 List Tasks

```http
GET /api/tasks/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Success

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

## 3.3 Task Detail

```http
GET /api/tasks/{id}/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Example

```http
GET /api/tasks/1/
```

### Status Codes

```text
200 OK
401 Unauthorized
404 Not Found
```

---

## 3.4 Update Task

```http
PUT /api/tasks/{id}/update/
```

### Authentication

Required.

### Manager

Can update any task.

### QA

Can update allowed tasks.

### Developer

Can update tasks assigned to/allowed for the developer.

### Request

```json
{
    "title": "Updated Login API",
    "description": "Updated task description"
}
```

### Success

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
403 Forbidden
404 Not Found
```

---

## 3.5 Delete Task

```http
DELETE /api/tasks/{id}/delete/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
```

### Denied Roles

```text
QA
Developer
```

### Success

```json
{
    "message": "Task deleted successfully"
}
```

### Status Codes

```text
200 OK / 204 No Content
401 Unauthorized
403 Forbidden
404 Not Found
```

---

## 3.6 Assign Task

```http
POST /api/tasks/{id}/assign/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
```

### Denied Roles

```text
QA
Developer
```

### Request

```json
{
    "assigned_to": 2
}
```

### Success

```json
{
    "message": "Task assigned successfully"
}
```

### Status Codes

```text
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
```

---

# 4. Document APIs

## 4.1 Upload Document

```http
POST /api/documents/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Content Type

```text
multipart/form-data
```

### Request

```text
title = Project Documentation
project = 1
file = documentation.pdf
```

### Success

```json
{
    "id": 1,
    "title": "Project Documentation",
    "project": 1,
    "file": "/media/documents/documentation.pdf"
}
```

### Status Codes

```text
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
```

---

## 4.2 List Documents

```http
GET /api/documents/list/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Success

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

## 4.3 Document Detail

```http
GET /api/documents/{id}/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Success

```json
{
    "id": 1,
    "title": "Project Documentation",
    "project": 1,
    "file": "/media/documents/documentation.pdf"
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

## 5.1 Create Comment

```http
POST /api/comments/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Request

```json
{
    "project": 1,
    "content": "This project is progressing well."
}
```

### Success

```json
{
    "id": 1,
    "project": 1,
    "content": "This project is progressing well."
}
```

### Status Codes

```text
201 Created
400 Bad Request
401 Unauthorized
```

---

## 5.2 List Comments

```http
GET /api/comments/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Status Codes

```text
200 OK
401 Unauthorized
```

---

## 5.3 Comment Detail

```http
GET /api/comments/{id}/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Success

```json
{
    "id": 1,
    "project": 1,
    "content": "This project is progressing well."
}
```

### Status Codes

```text
200 OK
401 Unauthorized
404 Not Found
```

---

## 5.4 Update Comment

```http
PUT /api/comments/{id}/
```

### Authentication

Required.

### Permission Rules

Manager:

```text
Can update any comment.
```

QA:

```text
Can update own comments.
```

Developer:

```text
Can update own comments.
```

### Request

```json
{
    "content": "Updated project comment."
}
```

### Success

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
403 Forbidden
404 Not Found
```

---

## 5.5 Delete Comment

```http
DELETE /api/comments/{id}/
```

### Authentication

Required.

### Permission Rules

Manager:

```text
Can delete any comment.
```

QA:

```text
Can delete own comments.
```

Developer:

```text
Can delete own comments.
```

### Success

```json
{
    "message": "Comment deleted successfully"
}
```

### Status Codes

```text
200 OK / 204 No Content
401 Unauthorized
403 Forbidden
404 Not Found
```

---

## 5.6 Project Comments

```http
GET /api/projects/{id}/comments/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Success

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
404 Not Found
```

---

# 6. Timeline APIs

## 6.1 List Timeline Events

```http
GET /api/timeline/
```

### Authentication

Required.

### Allowed Roles

```text
Manager
QA
Developer
```

### Success

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

## 7.1 List Notifications

```http
GET /api/notifications/
```

### Authentication

Required.

### Permission

Users can access their own notifications.

### Allowed Roles

```text
Manager
QA
Developer
```

### Success

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

## 7.2 Mark Notification as Read

```http
PATCH /api/notifications/{id}/read/
```

### Authentication

Required.

### Permission

The authenticated user can mark their own notification as read.

A user cannot modify another user's notification.

### Success

```json
{
    "message": "Notification marked as read"
}
```

### Status Codes

```text
200 OK
401 Unauthorized
403 Forbidden
404 Not Found
```

---

# API Summary

|  # | API                    | Method | Authentication | Main Permission    |
| -: | ---------------------- | ------ | -------------- | ------------------ |
|  1 | Register               | POST   | No             | Public             |
|  2 | Login                  | POST   | No             | Public             |
|  3 | Logout                 | POST   | Yes            | Authenticated      |
|  4 | Create Project         | POST   | Yes            | Manager            |
|  5 | List Projects          | GET    | Yes            | All Roles          |
|  6 | Project Detail         | GET    | Yes            | All Roles          |
|  7 | Update Project         | PUT    | Yes            | Manager            |
|  8 | Delete Project         | DELETE | Yes            | Manager            |
|  9 | Create Task            | POST   | Yes            | Manager            |
| 10 | List Tasks             | GET    | Yes            | All Roles          |
| 11 | Task Detail            | GET    | Yes            | All Roles          |
| 12 | Update Task            | PUT    | Yes            | Role/Assignment    |
| 13 | Delete Task            | DELETE | Yes            | Manager            |
| 14 | Assign Task            | POST   | Yes            | Manager            |
| 15 | Upload Document        | POST   | Yes            | All Roles          |
| 16 | List Documents         | GET    | Yes            | All Roles          |
| 17 | Document Detail        | GET    | Yes            | All Roles          |
| 18 | Create Comment         | POST   | Yes            | All Roles          |
| 19 | List Comments          | GET    | Yes            | All Roles          |
| 20 | Comment Detail         | GET    | Yes            | All Roles          |
| 21 | Update Comment         | PUT    | Yes            | Owner/Manager      |
| 22 | Delete Comment         | DELETE | Yes            | Owner/Manager      |
| 23 | Project Comments       | GET    | Yes            | All Roles          |
| 24 | Timeline Events        | GET    | Yes            | All Roles          |
| 25 | Notifications          | GET    | Yes            | Own Notifications  |
| 26 | Mark Notification Read | PATCH  | Yes            | Notification Owner |

---

# HTTP Status Codes

| Status | Meaning                                       |
| -----: | --------------------------------------------- |
|    200 | Request successful                            |
|    201 | Resource created                              |
|    204 | Resource deleted successfully                 |
|    400 | Bad Request                                   |
|    401 | Authentication required / invalid credentials |
|    403 | Authenticated but permission denied           |
|    404 | Resource not found                            |
|    405 | Method not allowed                            |
|    500 | Internal server error                         |

---

# Authentication vs Authorization

## Authentication

Authentication checks whether the user has a valid JWT token.

Example:

```text
No JWT
   ↓
401 Unauthorized
```

## Authorization

Authorization checks whether the authenticated user has permission to perform the requested operation.

Example:

```text
Valid JWT
   ↓
Developer
   ↓
POST /api/projects/
   ↓
Project creation requires Manager
   ↓
403 Forbidden
```

---

# Authorization Test Cases

The application should test both successful and denied operations.

## Authentication Tests

### Registration

```text
test_register_user
test_duplicate_username
test_password_mismatch
test_missing_required_field
```

### Login

```text
test_login_success
test_login_invalid_credentials
```

### Logout

```text
test_logout_success
test_logout_invalid_refresh_token
```

---

# Project Permission Tests

```text
test_manager_can_create_project
test_qa_cannot_create_project
test_developer_cannot_create_project

test_all_roles_can_list_projects
test_all_roles_can_view_project

test_manager_can_update_project
test_qa_cannot_update_project
test_developer_cannot_update_project

test_manager_can_delete_project
test_qa_cannot_delete_project
test_developer_cannot_delete_project
```

Expected denied response:

```text
403 Forbidden
```

---

# Task Permission Tests

```text
test_manager_can_create_task
test_qa_cannot_create_task
test_developer_cannot_create_task

test_all_roles_can_list_tasks
test_all_roles_can_view_task

test_manager_can_update_task
test_qa_can_update_allowed_task
test_developer_can_update_assigned_task

test_unauthorized_user_cannot_update_task

test_manager_can_delete_task
test_qa_cannot_delete_task
test_developer_cannot_delete_task

test_manager_can_assign_task
test_qa_cannot_assign_task
test_developer_cannot_assign_task
```

---

# Document Permission Tests

```text
test_manager_can_upload_document
test_qa_can_upload_document
test_developer_can_upload_document

test_all_roles_can_list_documents
test_all_roles_can_view_document

test_unauthenticated_cannot_access_documents
```

---

# Comment Permission Tests

```text
test_manager_can_create_comment
test_qa_can_create_comment
test_developer_can_create_comment

test_all_roles_can_list_comments
test_all_roles_can_view_comment

test_manager_can_update_any_comment

test_qa_can_update_own_comment
test_developer_can_update_own_comment

test_qa_cannot_update_other_user_comment
test_developer_cannot_update_other_user_comment

test_manager_can_delete_any_comment

test_qa_can_delete_own_comment
test_developer_can_delete_own_comment

test_qa_cannot_delete_other_user_comment
test_developer_cannot_delete_other_user_comment
```

---

# Timeline Permission Tests

```text
test_manager_can_view_timeline
test_qa_can_view_timeline
test_developer_can_view_timeline
test_unauthenticated_cannot_view_timeline
```

---

# Notification Permission Tests

```text
test_manager_can_view_own_notifications
test_qa_can_view_own_notifications
test_developer_can_view_own_notifications

test_manager_can_mark_own_notification_read
test_qa_can_mark_own_notification_read
test_developer_can_mark_own_notification_read

test_user_cannot_access_other_user_notification
test_user_cannot_mark_other_user_notification_read
```

---

# General Authorization Tests

Every protected endpoint should verify:

### No authentication

Expected:

```text
401 Unauthorized
```

### Authentication with wrong role

Expected:

```text
403 Forbidden
```

### Authentication with correct role

Expected:

```text
200 OK
201 Created
204 No Content
```

depending on the operation.

### Ownership protection

For resources such as comments and notifications:

```text
Correct owner
    ↓
Allowed

Different user
    ↓
403 Forbidden
```

---

# Swagger API Documentation

The project uses **DRF Spectacular**.

Swagger:

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

Swagger can be used to:

* View all endpoints
* View HTTP methods
* View request parameters
* View request bodies
* View response schemas
* Authorize JWT tokens
* Test APIs interactively

For protected endpoints, provide:

```text
Bearer ACCESS_TOKEN
```

---

# Complete API Flow

```text
Register
   ↓
Login
   ↓
Receive JWT Access + Refresh Token
   ↓
Authorize API Requests
   ↓
Role Checked
   ↓
Manager / QA / Developer
   ↓
Permission Checked
   ↓
Allowed Operation
   ↓
Create / Read / Update / Delete
   ↓
Timeline Event / Notification
   ↓
Logout
```

---

# Role-Based Authorization Flow

```text
Request
   ↓
JWT Authentication
   ↓
Is user authenticated?
   ├── No → 401 Unauthorized
   │
   └── Yes
        ↓
     Get Profile
        ↓
     Check Role
        ↓
     Is role allowed?
        ├── No → 403 Forbidden
        │
        └── Yes
             ↓
        Check Ownership
             ↓
        Permission Granted
             ↓
        Execute API
```

---

# Security Notes

Protected APIs must never rely only on authentication.

The application must verify:

```text
Authentication
+
Role
+
Ownership where applicable
```

This prevents users from performing operations outside their assigned responsibilities.

---

# Documentation Separation

The project follows this documentation structure:

### README.md

Contains:

* Project overview
* Features
* Technology stack
* Project structure
* Requirements
* Installation
* Virtual environment
* Dependencies
* Environment variables
* Database setup
* Superuser creation
* Running the server
* Testing setup
* Security
* Deployment
* Git workflow

### API_DOCUMENTATION.md

Contains:

* Base URL
* Authentication
* Authorization
* Roles
* Permission matrix
* API endpoints
* Request examples
* Response examples
* Status codes
* Authorization test cases
* Swagger documentation

This separation keeps installation and environment configuration out of the API reference documentation.
