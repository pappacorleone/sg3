def end_of_weekday_prompt(checklist, past_performance):
  # Predict likely tasks and habits that will be completed based on past performance
  likely_completed_tasks = []
  for task in checklist.tasks:
    if task.priority in past_performance:
      likely_completed_tasks.append(task)
  return likely_completed_tasks
