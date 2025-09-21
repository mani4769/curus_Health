class Project:
    def __init__(self, name, description, members=None, tasks=None):
        self.name = name
        self.description = description
        self.members = members or []
        self.tasks = tasks or []

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "members": self.members,
            "tasks": self.tasks
        }
