class Task:
    def __init__(self, title, description, assigned_to, status, deadline, comments=None):
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.status = status
        self.deadline = deadline
        self.comments = comments or []

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "deadline": self.deadline,
            "comments": self.comments
        }
