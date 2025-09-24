from flask import Flask, send_from_directory
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Disable strict slashes to fix 308 redirection issues
app.url_map.strict_slashes = False
# Update CORS to allow any origin and fix OPTIONS preflight
CORS(app, 
     origins=["*"], 
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "Accept"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
     automatic_options=True)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
jwt = JWTManager(app)

# MongoDB connection
try:
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'), serverSelectionTimeoutMS=5000)
    # Test the connection
    client.admin.command('ping')
    db = client[os.getenv('DATABASE_NAME', 'project_management_db')]
    print("✅ MongoDB connected successfully")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("⚠️  Running in demo mode without database")
    db = None

# Make db available to other modules
app.db = db

# Register routes
print("🔧 Registering blueprints...")
try:
    from routes.auth import auth_bp
    from routes.users import user_bp
    from routes.project import project_bp
    from routes.task import task_bp
    from routes.reports import report_bp
    from routes.ai import ai_bp
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)

try:
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(project_bp, url_prefix="/api/projects")
    app.register_blueprint(task_bp, url_prefix="/api/tasks")
    app.register_blueprint(report_bp, url_prefix="/api/reports")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    print("✅ All blueprints registered successfully")
except Exception as e:
    print(f"❌ Blueprint registration error: {e}")
    exit(1)

@app.route('/')
def health_check():
    return {"message": "Project Management API is running!", "status": "healthy"}

@app.route('/api/test')
def test_endpoint():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    return {"message": "API test endpoint working!", "routes": routes}

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    # In production, serve the built React app
    if os.path.exists('../frontend/build'):
        app.static_folder = '../frontend/build'
        print("✅ Serving built React frontend")
    else:
        print("⚠️  React build not found, serving API only")

    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
