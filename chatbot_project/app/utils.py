users = {}  # For demo purposes, using an in-memory dictionary

def check_login(username, password):
    return users.get(username) == password

def register_user(username, password):
    if username in users:
        return False  # Username already exists
    users[username] = password
    return True
