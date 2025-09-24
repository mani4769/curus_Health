from flask import Blueprint, request, jsonify, current_app
import os

ai_bp = Blueprint('ai', __name__)

# Initialize GROQ client safely
groq_client = None
groq_api_key = os.getenv('GROQ_API_KEY')

# Only import and initialize if we have a valid API key
if groq_api_key and groq_api_key != 'your-groq-api-key-here':
    try:
        from groq import Groq
        groq_client = Groq(api_key=groq_api_key)
        print("✅ GROQ client initialized successfully")
    except Exception as e:
        print(f"⚠️ Error initializing GROQ client: {e}")
        groq_client = None

@ai_bp.route('/generate-user-stories', methods=['POST'])
def generate_user_stories():
    """Generate user stories from project description using GROQ AI"""
    if not groq_client:
        return jsonify({"error": "GROQ API key not configured. Please set GROQ_API_KEY in your .env file."}), 503

    try:
        data = request.json
        project_description = data.get('projectDescription', '')
        project_id = data.get('projectId', '')

        if not project_description:
            return jsonify({"error": "Project description is required"}), 400

        # Create the prompt for user story generation
        prompt = f"""
        Generate detailed user stories from the following project description.
        Each user story should follow this exact format:
        "As a [role], I want to [action], so that [benefit]."

        Project Description: {project_description}

        Generate 5-10 user stories that cover the main functionality and user roles.
        Focus on different user types (customer, admin, user, etc.) and their needs.
        Make sure each story is specific and actionable.

        Return only the user stories as a JSON array of strings, no additional text.
        """

        # Call GROQ API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",  # Using Llama 3.1 8B Instant model
            temperature=0.7,
            max_tokens=1000,
        )

        # Extract the response
        response_text = chat_completion.choices[0].message.content.strip()

        # Try to parse as JSON, if not, split by newlines
        try:
            import json
            user_stories = json.loads(response_text)
        except:
            # Fallback: split by newlines and clean up
            user_stories = [line.strip().strip('"') for line in response_text.split('\n') if line.strip() and line.startswith('"')]

        # Store user stories in database if project_id provided
        if project_id and current_app.db:
            # Check if we should use demo mode
            use_demo_mode = (current_app.db is None or
                            current_app.db.projects.count_documents({}) == 0)

            if not use_demo_mode:
                # Store in database
                user_stories_doc = {
                    "project_id": project_id,
                    "description": project_description,
                    "stories": user_stories,
                    "generated_at": "2025-09-21T00:00:00Z"  # Current date
                }
                current_app.db.user_stories.insert_one(user_stories_doc)

        # Optional: Create tasks from user stories
        if data.get('createTasks', False) and project_id:
            create_tasks_from_stories(user_stories, project_id)

        return jsonify({
            "user_stories": user_stories,
            "count": len(user_stories),
            "project_id": project_id
        }), 200

    except Exception as e:
        print(f"Error generating user stories: {e}")
        return jsonify({"error": "Failed to generate user stories", "details": str(e)}), 500

def create_tasks_from_stories(user_stories, project_id):
    """Optional: Create tasks automatically from user stories"""
    try:
        use_demo_mode = (current_app.db is None or
                        current_app.db.projects.count_documents({}) == 0)

        if use_demo_mode:
            return  # Skip in demo mode

        for i, story in enumerate(user_stories):
            # Parse the user story to extract components
            # Format: "As a [role], I want to [action], so that [benefit]."
            if "As a" in story and "I want to" in story and "so that" in story:
                parts = story.split(", I want to ")
                if len(parts) == 2:
                    role_part = parts[0].replace("As a ", "")
                    action_benefit = parts[1].split(", so that ")
                    if len(action_benefit) == 2:
                        action = action_benefit[0]
                        benefit = action_benefit[1].rstrip(".")

                        # Create task
                        task_data = {
                            "project_id": project_id,
                            "title": f"Implement: {action}",
                            "description": f"User Story: {story}\n\nBenefit: {benefit}",
                            "status": "To Do",
                            "priority": "Medium",
                            "assigned_to": None,  # Unassigned
                            "deadline": None,  # No deadline
                            "comments": [],
                            "created_at": "2025-09-21T00:00:00Z",
                            "updated_at": "2025-09-21T00:00:00Z"
                        }
                        current_app.db.tasks.insert_one(task_data)

    except Exception as e:
        print(f"Error creating tasks from stories: {e}")

@ai_bp.route('/user-stories/<project_id>', methods=['GET'])
def get_user_stories(project_id):
    """Get generated user stories for a project"""
    try:
        use_demo_mode = (current_app.db is None or
                        current_app.db.projects.count_documents({}) == 0)

        if use_demo_mode:
            return jsonify([]), 200

        stories = list(current_app.db.user_stories.find({"project_id": project_id}))
        for story in stories:
            story["_id"] = str(story["_id"])

        return jsonify(stories), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch user stories"}), 500
