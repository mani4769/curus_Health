from flask import Blueprint, current_app
from datetime import datetime

report_bp = Blueprint('reports', __name__)

@report_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    # Check if we should use demo mode
    use_demo_mode = (current_app.db is None or 
                    current_app.db.projects.count_documents({}) == 0)
    
    if use_demo_mode:
        # Demo mode - return mock dashboard data
        return {
            "total_projects": 2,
            "total_tasks": 3,
            "total_users": 3,
            "overdue_tasks": 0,
            "completion_rate": 33,
            "tasks_by_status": {
                "To Do": 1,
                "In Progress": 1,
                "Done": 1
            },
            "recent_overdue_tasks": []
        }
    
    # Database mode
    total_projects = current_app.db.projects.count_documents({})
    total_tasks = current_app.db.tasks.count_documents({})
    total_users = current_app.db.users.count_documents({})
    
    # Tasks by status
    tasks_by_status = {}
    pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    status_results = list(current_app.db.tasks.aggregate(pipeline))
    for result in status_results:
        tasks_by_status[result["_id"]] = result["count"]
    
    # Overdue tasks
    from datetime import datetime
    now = datetime.utcnow()
    overdue_count = current_app.db.tasks.count_documents({
        "deadline": {"$lt": now},
        "status": {"$ne": "Done"}
    })
    
    # Completion rate
    done_tasks = tasks_by_status.get("Done", 0)
    completion_rate = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Recent overdue tasks
    recent_overdue = list(current_app.db.tasks.find({
        "deadline": {"$lt": now},
        "status": {"$ne": "Done"}
    }).sort("deadline", 1).limit(5))
    for task in recent_overdue:
        task["_id"] = str(task["_id"])
    
    return {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "total_users": total_users,
        "overdue_tasks": overdue_count,
        "completion_rate": round(completion_rate, 1),
        "tasks_by_status": tasks_by_status,
        "recent_overdue_tasks": recent_overdue
    }

@report_bp.route('/tasks-by-status', methods=['GET'])
def get_tasks_by_status():
    # Check if we should use demo mode
    use_demo_mode = (current_app.db is None or 
                    current_app.db.tasks.count_documents({}) == 0)
    
    if use_demo_mode:
        return {
            "To Do": 1,
            "In Progress": 1,
            "Done": 1
        }
    
    # Database mode
    pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    results = list(current_app.db.tasks.aggregate(pipeline))
    tasks_by_status = {}
    for result in results:
        tasks_by_status[result["_id"]] = result["count"]
    return tasks_by_status

@report_bp.route('/overdue-tasks', methods=['GET'])
def get_overdue_tasks():
    # Check if we should use demo mode
    use_demo_mode = (current_app.db is None or 
                    current_app.db.tasks.count_documents({}) == 0)
    
    if use_demo_mode:
        return []
    
    # Database mode
    from datetime import datetime
    now = datetime.utcnow()
    overdue_tasks = list(current_app.db.tasks.find({
        "deadline": {"$lt": now},
        "status": {"$ne": "Done"}
    }))
    for task in overdue_tasks:
        task["_id"] = str(task["_id"])
    return overdue_tasks

@report_bp.route('/user-workload', methods=['GET'])
def get_user_workload():
    # Check if we should use demo mode
    use_demo_mode = (current_app.db is None or 
                    current_app.db.tasks.count_documents({}) == 0)
    
    if use_demo_mode:
        return {
            "demo-developer": 3
        }
    
    # Database mode
    pipeline = [
        {"$group": {"_id": "$assigned_to", "count": {"$sum": 1}}}
    ]
    results = list(current_app.db.tasks.aggregate(pipeline))
    user_workload = {}
    for result in results:
        user_workload[str(result["_id"])] = result["count"]
    return user_workload
