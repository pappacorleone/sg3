class Checklist:
  def __init__(self, name, description):
    self.name = name
    self.description = description
    self.tasks = []
    self.habits = []

class ChecklistDatabase:
  def __init__(self):
    self.checklists = []

  def add_checklist(self, name, description):
    checklist = Checklist(name, description)
    self.checklists.append(checklist)
    return checklist

  def get_checklist(self, name):
    for checklist in self.checklists:
      if checklist.name == name:
        return checklist
    return None

  def delete_checklist(self, checklist):
    self.checklists.remove(checklist)

