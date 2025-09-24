# Create demo users for testing
from pymongo import MongoClient
import bcrypt
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('DATABASE_NAME')]

def create_demo_users():
    """Create demo users for testing"""
    users_collection = db.users
    
    # Check if users already exist
    if users_collection.count_documents({}) > 0:
        print("Users already exist. Skipping creation.")
        return
    
    demo_users = [
        {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "admin123",
            "role": "Admin"
        },
        {
            "name": "Manager User",
            "email": "manager@example.com", 
            "password": "manager123",
            "role": "Manager"
        },
        {
            "name": "Developer User",
            "email": "dev@example.com",
            "password": "dev123", 
            "role": "Developer"
        }
    ]
    
    for user_data in demo_users:
        # Hash password
        hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
        
        user = {
            "name": user_data['name'],
            "email": user_data['email'],
            "role": user_data['role'],
            "password": hashed_password,
            "created_at": datetime.utcnow()
        }
        
        result = users_collection.insert_one(user)
        print(f"Created user: {user_data['name']} ({user_data['email']}) with ID: {result.inserted_id}")

def create_demo_projects():
    """Create demo projects"""
    projects_collection = db.projects
    users_collection = db.users
    
    # Get admin user
    admin_user = users_collection.find_one({"role": "Admin"})
    manager_user = users_collection.find_one({"role": "Manager"})
    dev_user = users_collection.find_one({"role": "Developer"})
    
    if not admin_user or not manager_user or not dev_user:
        print("Demo users not found. Please create users first.")
        return
    
    demo_projects = [
        {
            "name": "E-commerce Website",
            "description": "Build a modern e-commerce platform with React and Node.js",
            "created_by": admin_user['_id'],
            "team": [manager_user['_id'], dev_user['_id']],
            "deadline": datetime(2025, 12, 31),
            "status": "Active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Mobile App Development", 
            "description": "Create a cross-platform mobile app using React Native",
            "created_by": manager_user['_id'],
            "team": [dev_user['_id']],
            "deadline": datetime(2025, 11, 15),
            "status": "Active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    for project_data in demo_projects:
        result = projects_collection.insert_one(project_data)
        print(f"Created project: {project_data['name']} with ID: {result.inserted_id}")

def create_demo_tasks():
    """Create demo tasks"""
    tasks_collection = db.tasks
    projects_collection = db.projects
    users_collection = db.users
    
    # Get first project and dev user
    project = projects_collection.find_one()
    dev_user = users_collection.find_one({"role": "Developer"})
    
    if not project or not dev_user:
        print("Demo project or user not found.")
        return
    
    demo_tasks = [
        {
            "project_id": project['_id'],
            "title": "Setup project structure",
            "description": "Initialize the project with proper folder structure and dependencies",
            "assigned_to": dev_user['_id'],
            "status": "Done",
            "priority": "High",
            "deadline": datetime(2025, 10, 15),
            "comments": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "project_id": project['_id'],
            "title": "Design user interface",
            "description": "Create wireframes and mockups for the main pages",
            "assigned_to": dev_user['_id'],
            "status": "In Progress", 
            "priority": "Medium",
            "deadline": datetime(2025, 10, 30),
            "comments": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "project_id": project['_id'],
            "title": "Implement authentication",
            "description": "Add user login, signup and JWT-based authentication",
            "assigned_to": dev_user['_id'],
            "status": "To Do",
            "priority": "High", 
            "deadline": datetime(2025, 11, 5),
            "comments": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    for task_data in demo_tasks:
        result = tasks_collection.insert_one(task_data)
        print(f"Created task: {task_data['title']} with ID: {result.inserted_id}")

if __name__ == "__main__":
    print("Creating demo data...")
    create_demo_users()
    create_demo_projects()
    create_demo_tasks()
    print("Demo data creation completed!")
