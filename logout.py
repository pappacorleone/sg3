from requests import session

def logout():
  # Clear user's session
  session.clear()