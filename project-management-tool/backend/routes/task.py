from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/', methods=['GET'])
def get_tasks():
    # Check if we should use demo mode
    use_demo_mode = (current_app.db is None or 
                    current_app.db.tasks.count_documents({}) == 0)
    
    if use_demo_mode:
        # Demo mode - return mock tasks
        return jsonify([
            {
                "_id": "demo-task-1",
                "title": "Setup project structure",
                "description": "Initialize the project with proper folder structure and dependencies",
                "status": "Done",
                "priority": "High",
                "assigned_to": "demo-developer",
                "project_id": "demo-project-1",
                "deadline": "2025-10-15T00:00:00Z",
                "comments": [],
                "created_at": "2025-09-20T00:00:00Z"
            },
            {
                "_id": "demo-task-2",
                "title": "Design user interface", 
                "description": "Create wireframes and mockups for the main pages",
                "status": "In Progress",
                "priority": "Medium",
                "assigned_to": "demo-designer",
                "project_id": "demo-project-1",
                "deadline": "2025-10-30T00:00:00Z",
                "comments": [],
                "created_at": "2025-09-20T00:00:00Z"
            },
            {
                "_id": "demo-task-3",
                "title": "Implement authentication",
                "description": "Add user login, signup and JWT-based authentication",
                "status": "To Do",
                "priority": "High",
                "assigned_to": "demo-developer", 
                "project_id": "demo-project-1",
                "deadline": "2025-11-05T00:00:00Z",
                "comments": [],
                "created_at": "2025-09-20T00:00:00Z"
            },
            {
                "_id": "demo-task-4",
                "title": "Setup mobile app framework",
                "description": "Initialize React Native project with navigation and basic screens",
                "status": "Done",
                "priority": "High",
                "assigned_to": "demo-developer",
                "project_id": "demo-project-2",
                "deadline": "2025-09-25T00:00:00Z",
                "comments": [],
                "created_at": "2025-09-20T00:00:00Z"
            },
            {
                "_id": "demo-task-5",
                "title": "Design app UI components",
                "description": "Create reusable UI components for the mobile app",
                "status": "In Progress",
                "priority": "Medium",
                "assigned_to": "demo-designer",
                "project_id": "demo-project-2",
                "deadline": "2025-10-10T00:00:00Z",
                "comments": [],
                "created_at": "2025-09-21T00:00:00Z"
            },
            {
                "_id": "demo-task-6",
                "title": "Implement data visualization",
                "description": "Build charts and graphs for the analytics dashboard",
                "status": "To Do",
                "priority": "High",
                "assigned_to": "demo-developer",
                "project_id": "demo-project-3",
                "deadline": "2025-12-15T00:00:00Z",
                "comments": [],
                "created_at": "2025-09-21T00:00:00Z"
            },
            {
                "_id": "demo-task-7",
                "title": "Integrate AI chatbot API",
                "description": "Connect to AI service and implement chat functionality",
                "status": "Planning",
                "priority": "Medium",
                "assigned_to": "demo-developer",
                "project_id": "demo-project-4",
                "deadline": "2025-10-20T00:00:00Z",
                "comments": [],
                "created_at": "2025-09-21T00:00:00Z"
            },
            {
                "_id": "demo-task-8",
                "title": "Write unit tests",
                "description": "Create comprehensive unit tests for all components",
                "status": "To Do",
                "priority": "Low",
                "assigned_to": "demo-tester",
                "project_id": "demo-project-1",
                "deadline": "2025-11-20T00:00:00Z",
                "comments": [],
                "created_at": "2025-09-22T00:00:00Z"
            }
        ])
    
    tasks = list(current_app.db.tasks.find())
    for task in tasks:
        task["_id"] = str(task["_id"])
        if "project_id" in task:
            task["project_id"] = str(task["project_id"])
        if "assigned_to" in task:
            task["assigned_to"] = str(task["assigned_to"])
    return jsonify(tasks)

@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.json
    current_app.db.tasks.insert_one(data)
    return jsonify({"message": "Task created"}), 201

@task_bp.route('/<task_id>', methods=['GET'])
def get_task(task_id):
    from bson import ObjectId
    task = current_app.db.tasks.find_one({"_id": ObjectId(task_id)})
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task["_id"] = str(task["_id"])
    if "project_id" in task:
        task["project_id"] = str(task["project_id"])
    if "assigned_to" in task:
        task["assigned_to"] = str(task["assigned_to"])
    return jsonify(task)

@task_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    from bson import ObjectId
    result = current_app.db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task updated"}), 200

@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    from bson import ObjectId
    result = current_app.db.tasks.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted"}), 200

@task_bp.route('/<task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    data = request.json
    status = data.get("status")
    if not status:
        return jsonify({"error": "Status required"}), 400
    from bson import ObjectId
    result = current_app.db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": status}}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task status updated"}), 200

@task_bp.route('/<task_id>/comments', methods=['POST'])
def add_comment(task_id):
    data = request.json
    comment = data.get("comment")
    if not comment:
        return jsonify({"error": "Comment required"}), 400
    from bson import ObjectId
    result = current_app.db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$push": {"comments": comment}}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Comment added"}), 200
