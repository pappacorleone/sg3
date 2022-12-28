def select_task_habit(checklist, past_performance, user_preferences):
  # Recommend tasks and habits based on past performance and user preferences
  recommended_tasks = []
  recommended_habits = []
  for task in checklist.tasks:
    if task.priority in past_performance:
      recommended_tasks.append(task)
  for habit in checklist.habits:
    if habit.frequency in user_preferences:
      recommended_habits.append(habit)
  return recommended_tasks, recommended_habits
