# Collaborative Project Management API

A professional RESTful backend API for a collaborative project management system built with **Django** and **Django REST Framework (DRF)**.

The system is designed to provide project management functionality similar to platforms such as **Jira, GitHub Issues, and YouTrack**, allowing teams to manage projects, tasks, tickets, documents, comments, timelines, and notifications through secure REST APIs.

---

## 🚀 Features

- User registration and authentication
- JWT-based authentication
- User logout with refresh-token blacklisting
- User profiles
- Profile picture upload
- Role-based user profiles
- Project management
- Project team members
- Task management
- Task assignment
- Task status management
- Project document management
- Custom document version field
- Comments and discussions
- Timeline events
- User notifications
- Mark notifications as read
- Ticket / issue management
- Project-based access validation
- Team-member validation
- API-level validation
- RESTful API architecture

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| Django REST Framework | REST API development |
| Simple JWT | Authentication |
| SQLite | Development database |
| Pillow | Image/file processing |
| Git | Version control |
| GitHub | Source code management |
| Postman | API testing |

---

# 📁 Project Structure

```text
Project ManagemetAPI/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── media/
│
├── static/
│
├── manage.py
├── requirements.txt
└── README.md
