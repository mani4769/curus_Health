from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    print("🔍 Login request received")
    print(f"Request data: {request.json}")
    
    data = request.json
    
    # Check if we should use demo mode (no DB or empty DB)
    use_demo_mode = (current_app.db is None or 
                    current_app.db.users.count_documents({}) == 0)
    
    if use_demo_mode:
        print("📝 Running in demo mode")
        # Demo mode - accept any login with demo credentials
        demo_users = {
            "admin@example.com": {"username": "Admin User", "role": "Admin"},
            "manager@example.com": {"username": "Manager User", "role": "Manager"}, 
            "dev@example.com": {"username": "Developer User", "role": "Developer"}
        }
        
        if data["email"] in demo_users:
            user_info = demo_users[data["email"]]
            token = create_access_token(identity={"email": data["email"], "role": user_info["role"]})
            return jsonify({
                "access_token": token,
                "user": {
                    "_id": f"demo-{data['email'].split('@')[0]}",
                    "username": user_info["username"],
                    "email": data["email"],
                    "role": user_info["role"]
                }
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    
    # Database mode
    print(f"🔍 Looking for user with email: {data.get('email')}")
    user = current_app.db.users.find_one({"email": data["email"]})
    if user and check_password_hash(user["password_hash"], data["password"]):
        token = create_access_token(identity={"email": user["email"], "role": user["role"]})
        return jsonify({
            "access_token": token,
            "user": {
                "_id": str(user["_id"]),
                "username": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }), 200
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/test', methods=['GET'])
@cross_origin()
def test_auth():
    return jsonify({"message": "Auth endpoint is working!", "method": "GET"})
