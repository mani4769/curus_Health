from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role
        }
