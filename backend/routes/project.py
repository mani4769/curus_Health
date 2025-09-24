from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId

project_bp = Blueprint('projects', __name__)

@project_bp.route('/', methods=['GET'])
def get_projects():
    # Check if we should use demo mode
    use_demo_mode = (current_app.db is None or 
                    current_app.db.projects.count_documents({}) == 0)
    
    if use_demo_mode:
        # Demo mode - return mock projects
        return jsonify([
            {
                "_id": "demo-project-1",
                "name": "E-commerce Website",
                "description": "Build a modern e-commerce platform with React and Node.js",
                "status": "Active",
                "deadline": "2025-12-31T00:00:00Z",
                "team_members": ["demo-manager", "demo-developer", "demo-designer"],
                "created_by": "demo-admin",
                "created_at": "2025-09-20T00:00:00Z"
            },
            {
                "_id": "demo-project-2",
                "name": "Mobile App Development",
                "description": "Create a cross-platform mobile app using React Native",
                "status": "Active", 
                "deadline": "2025-11-15T00:00:00Z",
                "team_members": ["demo-developer", "demo-designer"],
                "created_by": "demo-manager",
                "created_at": "2025-09-20T00:00:00Z"
            },
            {
                "_id": "demo-project-3",
                "name": "Data Analytics Dashboard",
                "description": "Develop a comprehensive analytics dashboard for business intelligence",
                "status": "Planning",
                "deadline": "2026-01-20T00:00:00Z",
                "team_members": ["demo-developer", "demo-tester"],
                "created_by": "demo-admin",
                "created_at": "2025-09-21T00:00:00Z"
            },
            {
                "_id": "demo-project-4",
                "name": "AI Chatbot Implementation",
                "description": "Integrate AI-powered chatbot for customer support",
                "status": "In Progress",
                "deadline": "2025-10-30T00:00:00Z",
                "team_members": ["demo-developer", "demo-manager"],
                "created_by": "demo-manager",
                "created_at": "2025-09-21T00:00:00Z"
            }
        ])
    
    projects = list(current_app.db.projects.find())
    for project in projects:
        project["_id"] = str(project["_id"])
        if "team" in project:
            project["team"] = [str(member) for member in project["team"]]
        if "created_by" in project:
            project["created_by"] = str(project["created_by"])
    return jsonify(projects)

@project_bp.route('/', methods=['POST'])
def create_project():
    data = request.json
    if not data.get("name") or not data.get("description"):
        return jsonify({"error": "Missing required fields"}), 400
    current_app.db.projects.insert_one(data)
    return jsonify({"message": "Project created"}), 201

@project_bp.route('/<project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.json
    from bson import ObjectId
    result = current_app.db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"message": "Project updated"}), 200

@project_bp.route('/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    from bson import ObjectId
    result = current_app.db.projects.delete_one({"_id": ObjectId(project_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"message": "Project deleted"}), 200

@project_bp.route('/<project_id>/team', methods=['POST'])
def add_team_member(project_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    from bson import ObjectId
    result = current_app.db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$addToSet": {"team": ObjectId(user_id)}}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"message": "Team member added"}), 200

@project_bp.route('/<project_id>/team/<user_id>', methods=['DELETE'])
def remove_team_member(project_id, user_id):
    from bson import ObjectId
    result = current_app.db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$pull": {"team": ObjectId(user_id)}}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"message": "Team member removed"}), 200
