from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    # Check if we should use demo mode
    use_demo_mode = (current_app.db is None or 
                    current_app.db.users.count_documents({}) == 0)
    
    if use_demo_mode:
        # Demo mode - return mock users
        return jsonify([
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
            },
            {
                "_id": "demo-developer",
                "username": "Developer User", 
                "email": "dev@example.com",
                "role": "Developer",
                "created_at": "2025-09-20T00:00:00Z"
            },
            {
                "_id": "demo-designer",
                "username": "Designer User",
                "email": "designer@example.com",
                "role": "Designer",
                "created_at": "2025-09-21T00:00:00Z"
            },
            {
                "_id": "demo-tester",
                "username": "Tester User",
                "email": "tester@example.com",
                "role": "Tester",
                "created_at": "2025-09-21T00:00:00Z"
            }
        ])
    
    users = list(current_app.db.users.find({}, {"password_hash": 0}))
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify(users)

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400
    current_app.db.users.insert_one(data)
    return jsonify({"message": "User created"}), 201

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    from bson import ObjectId
    user = current_app.db.users.find_one({"_id": ObjectId(user_id)}, {"password_hash": 0})
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["_id"] = str(user["_id"])
    return jsonify(user)

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    # Check if demo mode
    use_demo_mode = (current_app.db is None or 
                    current_app.db.users.count_documents({}) == 0)
    
    if use_demo_mode:
        # Demo mode - just return success
        return jsonify({"message": "User updated (demo mode)"}), 200
    
    data = request.json
    from bson import ObjectId
    result = current_app.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User updated"}), 200

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Check if demo mode
    use_demo_mode = (current_app.db is None or 
                    current_app.db.users.count_documents({}) == 0)
    
    if use_demo_mode:
        # Demo mode - just return success
        return jsonify({"message": "User deleted (demo mode)"}), 200
    
    from bson import ObjectId
    result = current_app.db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200

@user_bp.route('/profile', methods=['GET'])
def get_profile():
    # This would require JWT, but for now return current user
    return jsonify({"message": "Profile endpoint"}), 200
