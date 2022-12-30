from checklist_database import ChecklistDatabase


def carryover(user, checklist):
  # Retrieve the user's checklist
  user_checklist = ChecklistDatabase.get_checklist(user)
  carryover_tasks = []
  for task in user_checklist.tasks:
    if task.status == 'incomplete':
      carryover_tasks.append(task)
  for habit in user_checklist.habits:
    if habit.status == 'incomplete':
      carryover_tasks.append(habit)
  user_checklist.tasks = carryover_tasks