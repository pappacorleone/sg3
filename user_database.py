import hashlib

class User:
  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password

class UserDatabase:
  def __init__(self):
    self.users = {}

  def add_user(self, name, email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = User(name, email, hashed_password)
    self.users[email] = user

  def authenticate(self, email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if email in self.users and self.users[email].password == hashed_password:
      return True
    return False
