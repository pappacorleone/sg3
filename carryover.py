def carryover(checklist):
  carryover_tasks = []
  for task in checklist.tasks:
    if task.status == 'incomplete':
      carryover_tasks.append(task)
  for habit in checklist.habits:
    if habit.status == 'incomplete':
      carryover_tasks.append(habit)
  checklist.tasks = carryover_tasks
