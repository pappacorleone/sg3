class Checklist:
  def __init__(self, name, description):
    self.name = name
    self.description = description
    self.tasks = []
    self.habits = []

class ChecklistDatabase:
  def __init__(self):
    self.checklists = {}

  def add_checklist(self, user, name, description):
    checklist = Checklist(name, description)
    if user in self.checklists:
      self.checklists[user].append(checklist)
    else:
      self.checklists[user] = [checklist]
    return checklist

  def get_checklist(self, user, name):
    if user in self.checklists:
      for checklist in self.checklists[user]:
        if checklist.name == name:
          return checklist
    return None

  def delete_checklist(self, user, checklist):
    if user in self.checklists:
      self.checklists[user].remove(checklist)

