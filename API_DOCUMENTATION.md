# Project Management Tool - API Documentation

## Base URL
http://localhost:5000

## Authentication
All API requests (except login) require a Bearer token in the Authorization header.

### Login
**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "_id": "demo-admin",
    "username": "Admin User",
    "email": "admin@example.com",
    "role": "Admin"
  }
}
```

**Demo Credentials:**
- Admin: `admin@example.com` / `admin123`
- Manager: `manager@example.com` / `manager123`
- Developer: `dev@example.com` / `dev123`
- Designer: `designer@example.com` / `designer123`
- Tester: `tester@example.com` / `tester123`

---

## Users API

### Get All Users
**Endpoint:** `GET /api/users`

**Response (200 OK):**
```json
[
  {
    "_id": "demo-admin",
    "username": "Admin User",
    "email": "admin@example.com",
    "role": "Admin",
    "created_at": "2025-09-20T00:00:00Z"
  },
  {
    "_id": "demo-manager",
    "username": "Manager User",
    "email": "manager@example.com",
    "role": "Manager",
    "created_at": "2025-09-20T00:00:00Z"
  }
]
```

### Create User
**Endpoint:** `POST /api/users`

**Request Body:**
```json
{
  "username": "New User",
  "email": "newuser@example.com",
  "password": "password123",
  "role": "Developer"
}
```

**Response (201 Created):**
```json
{
  "message": "User created"
}
```

### Update User
**Endpoint:** `PUT /api/users/{user_id}`

**Request Body:**
```json
{
  "username": "Updated User",
  "email": "updated@example.com",
  "role": "Manager"
}
```

**Response (200 OK):**
```json
{
  "message": "User updated"
}
```

### Delete User
**Endpoint:** `DELETE /api/users/{user_id}`

**Response (200 OK):**
```json
{
  "message": "User deleted"
}
```

---

## Projects API

### Get All Projects
**Endpoint:** `GET /api/projects`

**Response (200 OK):**
```json
[
  {
    "_id": "demo-project-1",
    "name": "E-commerce Website",
    "description": "Build a modern e-commerce platform",
    "status": "Active",
    "deadline": "2025-12-31T00:00:00Z",
    "team_members": ["demo-manager", "demo-developer"],
    "created_by": "demo-admin",
    "created_at": "2025-09-20T00:00:00Z"
  }
]
```

### Create Project
**Endpoint:** `POST /api/projects`

**Request Body:**
```json
{
  "name": "New Project",
  "description": "Project description",
  "status": "Active",
  "deadline": "2025-12-31T00:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "message": "Project created"
}
```

### Update Project
**Endpoint:** `PUT /api/projects/{project_id}`

**Request Body:**
```json
{
  "name": "Updated Project",
  "description": "Updated description",
  "status": "Completed"
}
```

**Response (200 OK):**
```json
{
  "message": "Project updated"
}
```

### Delete Project
**Endpoint:** `DELETE /api/projects/{project_id}`

**Response (200 OK):**
```json
{
  "message": "Project deleted"
}
```

### Add Team Member
**Endpoint:** `POST /api/projects/{project_id}/team`

**Request Body:**
```json
{
  "user_id": "demo-developer"
}
```

**Response (200 OK):**
```json
{
  "message": "Team member added"
}
```

### Remove Team Member
**Endpoint:** `DELETE /api/projects/{project_id}/team/{user_id}`

**Response (200 OK):**
```json
{
  "message": "Team member removed"
}
```

---

## Tasks API

### Get All Tasks
**Endpoint:** `GET /api/tasks`

**Query Parameters (optional):**
- `status`: Filter by status
- `assigned_to`: Filter by user ID
- `project_id`: Filter by project ID

**Response (200 OK):**
```json
[
  {
    "_id": "demo-task-1",
    "title": "Setup project structure",
    "description": "Initialize the project with proper folder structure",
    "status": "Done",
    "priority": "High",
    "assigned_to": "demo-developer",
    "project_id": "demo-project-1",
    "deadline": "2025-10-15T00:00:00Z",
    "comments": [],
    "created_at": "2025-09-20T00:00:00Z"
  }
]
```

### Create Task
**Endpoint:** `POST /api/tasks`

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "status": "To Do",
  "priority": "Medium",
  "assigned_to": "demo-developer",
  "project_id": "demo-project-1",
  "deadline": "2025-10-15T00:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "message": "Task created"
}
```

### Get Task by ID
**Endpoint:** `GET /api/tasks/{task_id}`

**Response (200 OK):**
```json
{
  "_id": "demo-task-1",
  "title": "Setup project structure",
  "description": "Initialize the project with proper folder structure",
  "status": "Done",
  "priority": "High",
  "assigned_to": "demo-developer",
  "project_id": "demo-project-1",
  "deadline": "2025-10-15T00:00:00Z",
  "comments": [],
  "created_at": "2025-09-20T00:00:00Z"
}
```

### Update Task
**Endpoint:** `PUT /api/tasks/{task_id}`

**Request Body:**
```json
{
  "title": "Updated Task",
  "status": "In Progress",
  "priority": "High"
}
```

**Response (200 OK):**
```json
{
  "message": "Task updated"
}
```

### Delete Task
**Endpoint:** `DELETE /api/tasks/{task_id}`

**Response (200 OK):**
```json
{
  "message": "Task deleted"
}
```

### Update Task Status
**Endpoint:** `PATCH /api/tasks/{task_id}/status`

**Request Body:**
```json
{
  "status": "Done"
}
```

**Response (200 OK):**
```json
{
  "message": "Task status updated"
}
```

### Add Comment to Task
**Endpoint:** `POST /api/tasks/{task_id}/comments`

**Request Body:**
```json
{
  "comment": "This is a new comment"
}
```

**Response (200 OK):**
```json
{
  "message": "Comment added"
}
```

---

## Reports API

### Get Dashboard Data
**Endpoint:** `GET /api/reports/dashboard`

**Response (200 OK):**
```json
{
  "total_projects": 4,
  "total_tasks": 8,
  "total_users": 5,
  "overdue_tasks": 0,
  "completion_rate": 25.0,
  "tasks_by_status": {
    "To Do": 4,
    "In Progress": 2,
    "Done": 2
  },
  "recent_overdue_tasks": []
}
```

### Get Tasks by Status
**Endpoint:** `GET /api/reports/tasks-by-status`

**Response (200 OK):**
```json
{
  "To Do": 4,
  "In Progress": 2,
  "Done": 2,
  "Planning": 1
}
```

### Get Overdue Tasks
**Endpoint:** `GET /api/reports/overdue-tasks`

**Response (200 OK):**
```json
[
  {
    "_id": "demo-task-1",
    "title": "Overdue Task",
    "deadline": "2025-09-15T00:00:00Z",
    "status": "To Do"
  }
]
```

### Get User Workload
**Endpoint:** `GET /api/reports/user-workload`

**Response (200 OK):**
```json
{
  "demo-developer": 5,
  "demo-designer": 2,
  "demo-tester": 1
}
```

---

## AI API

### Generate User Stories
**Endpoint:** `POST /api/ai/generate-user-stories`

**Request Body:**
```json
{
  "projectDescription": "An ecommerce website where customers can browse products, add to cart, and make payments online. Admin should manage products and view orders.",
  "projectId": "demo-project-1", // Optional: link to project
  "createTasks": false // Optional: auto-create tasks from stories
}
```

**Response (200 OK):**
```json
{
  "user_stories": [
    "As a customer, I want to browse products, so that I can choose what to buy.",
    "As a customer, I want to add products to a cart, so that I can purchase them later.",
    "As an admin, I want to manage the product catalog, so that the website reflects correct inventory."
  ],
  "count": 3,
  "project_id": "demo-project-1"
}
```

### Get User Stories for Project
**Endpoint:** `GET /api/ai/user-stories/{project_id}`

**Response (200 OK):**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "project_id": "demo-project-1",
    "description": "An ecommerce website...",
    "stories": ["As a customer...", "As an admin..."],
    "generated_at": "2025-09-21T00:00:00Z"
  }
]
```

### 401 Unauthorized
```json
{
  "msg": "Missing Authorization Header"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 400 Bad Request
```json
{
  "error": "Missing required fields"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Demo Mode

When MongoDB is not connected or collections are empty, the API runs in demo mode with mock data. All operations return success responses but don't persist changes.

## Authentication Header

Include the JWT token in requests:
```
Authorization: Bearer <your_jwt_token>
```

## Content Type

All POST/PUT/PATCH requests require:
```
Content-Type: application/json
```</content>
<parameter name="filePath">c:\Users\manimaddy\curus_Health\curus_Health\project-management-tool\API_DOCUMENTATION.md
