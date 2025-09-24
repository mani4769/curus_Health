# Project Management Tool

A full-stack project management application built with Flask (backend) and React (frontend) for managing projects, tasks, and users.

## Features

- 🔐 User Authentication & Authorization
- 📊 Dashboard with Analytics
- 👥 User Management (Admin only)
- 📁 Project Management
- ✅ Task Management
- 📈 Reports & Analytics
- 🤖 AI-Powered User Story Generator
- 🎨 Modern, Cinematic UI

## Tech Stack

### Backend
- **Flask** - Python web framework
- **MongoDB** - NoSQL database
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React** - JavaScript library
- **TypeScript** - Type safety
- **Material-UI** - Component library
- **Axios** - HTTP client

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (local or cloud)
- Git
- GROQ API Key (for AI features)

## Installation & Setup

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project-management-tool/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**
   Create a `.env` file in the backend directory:
   ```env
   JWT_SECRET_KEY=your-secret-key-here
   MONGODB_URI=mongodb://localhost:27017
   DATABASE_NAME=project_management_db
   GROQ_API_KEY=your-groq-api-key-here
   ```

   **Note:** Get your GROQ API key from [https://console.groq.com/](https://console.groq.com/)

5. **Run demo data creation** (optional)
   ```bash
   python create_demo_data.py
   ```

6. **Start the backend server**
   ```bash
   python app.py
   ```
   Server will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```
   Frontend will run on `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `GET /api/auth/test` - Test auth endpoint

### Users (Admin only)
- `GET /api/users` - Get all users
- `POST /api/users` - Create new user
- `PUT /api/users/<user_id>` - Update user
- `DELETE /api/users/<user_id>` - Delete user
- `GET /api/users/<user_id>` - Get user by ID
- `GET /api/users/profile` - Get current user profile

### Projects
- `GET /api/projects` - Get all projects
- `POST /api/projects` - Create new project
- `PUT /api/projects/<project_id>` - Update project
- `DELETE /api/projects/<project_id>` - Delete project
- `POST /api/projects/<project_id>/team` - Add team member
- `DELETE /api/projects/<project_id>/team/<user_id>` - Remove team member

### Tasks
- `GET /api/tasks` - Get all tasks (with optional filters)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/<task_id>` - Get task by ID
- `PUT /api/tasks/<task_id>` - Update task
- `DELETE /api/tasks/<task_id>` - Delete task
- `PATCH /api/tasks/<task_id>/status` - Update task status
- `POST /api/tasks/<task_id>/comments` - Add comment to task

### Reports
- `GET /api/reports/dashboard` - Get dashboard data
- `GET /api/reports/tasks-by-status` - Get tasks grouped by status
- `GET /api/reports/overdue-tasks` - Get overdue tasks
- `GET /api/reports/user-workload` - Get user workload data

### AI Features
- `POST /api/ai/generate-user-stories` - Generate user stories using GROQ AI
- `GET /api/ai/user-stories/<project_id>` - Get generated user stories for a project

**Note:** GROQ models may be updated periodically. If you encounter model deprecation errors, check the latest available models at [https://console.groq.com/docs/models](https://console.groq.com/docs/models)

## Database Schema

### Collections

#### Users
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  password_hash: String,
  role: String, // "Admin", "Manager", "Developer", "Designer", "Tester"
  created_at: Date
}
```

#### Projects
```javascript
{
  _id: ObjectId,
  name: String,
  description: String,
  status: String, // "Active", "Planning", "Completed", "On Hold"
  deadline: Date,
  team: [ObjectId], // References to Users
  created_by: ObjectId, // Reference to User
  created_at: Date,
  updated_at: Date
}
```

#### Tasks
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  status: String, // "To Do", "In Progress", "Done", "Planning"
  priority: String, // "Low", "Medium", "High"
  assigned_to: ObjectId, // Reference to User
  project_id: ObjectId, // Reference to Project
  deadline: Date,
  comments: [String],
  created_at: Date,
  updated_at: Date
}
```

#### User Stories (AI Generated)
```javascript
{
  _id: ObjectId,
  project_id: ObjectId, // Reference to Project
  description: String, // Original project description
  stories: [String], // Array of generated user stories
  generated_at: Date
}
```

## Demo Credentials

- **Admin**: admin@example.com / admin123
- **Manager**: manager@example.com / manager123
- **Developer**: dev@example.com / dev123
- **Designer**: designer@example.com / designer123
- **Tester**: tester@example.com / tester123

## Assumptions

1. **Demo Mode**: When MongoDB is not available or collections are empty, the app runs in demo mode with mock data
2. **Role-based Access**: Only Admin users can manage users; all authenticated users can manage projects and tasks
3. **Single Database**: All data is stored in a single MongoDB database
4. **JWT Authentication**: Tokens are stored in localStorage and included in API requests
5. **CORS**: Frontend and backend run on different ports, CORS is enabled

## Possible Improvements

### Backend
- Add input validation and sanitization
- Implement rate limiting
- Add comprehensive error handling
- Add unit and integration tests
- Implement caching (Redis)
- Add email notifications
- Implement file upload for attachments
- Add audit logging

### Frontend
- Add form validation
- Implement real-time updates (WebSocket)
- Add drag-and-drop for task management
- Implement dark mode
- Add pagination for large datasets
- Add search and filtering
- Implement offline support (PWA)
- Add data export functionality

### Features
- Add time tracking for tasks
- Implement project templates
- Add team collaboration features (comments, mentions)
- Integrate with external tools (Slack, GitHub)
- Add reporting and analytics dashboard
- ✅ **AI-powered user story generation** (Implemented)
- Add calendar view for deadlines
- Implement notification system

### DevOps
- Docker containerization
- CI/CD pipeline
- Environment-specific configurations
- Database migrations
- Monitoring and logging
- Backup and recovery

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.</content>
<parameter name="filePath">c:\Users\manimaddy\curus_Health\curus_Health\project-management-tool\README.md


contact details:-

Name : - Thirumalla sai naga Manikanta
Phoe no :- 9381017897
mail:- manikantathiumalla342@gmail.com

