def select_task_habit(user_email, checklist, past_performance, user_preferences):
  # Recommend tasks and habits based on past performance and user preferences
  recommended_tasks = []
  recommended_habits = []
  for task in checklist.tasks:
    if task.priority in past_performance:
      recommended_tasks.append(task)
  for habit in checklist.habits:
    if habit.frequency in user_preferences:
      recommended_habits.append(habit)

  # Prompt the user to select which tasks and habits to carry out
  text = "Please select which tasks and habits you would like to complete for {}:\n\n".format(checklist.name)
  for i, task in enumerate(recommended_tasks):
    text += "{}. {}\n".format(i+1, task.name)
  for i, habit in enumerate(recommended_habits):
    text += "{}. {}\n".format(i+1+len(recommended_tasks), habit.name)
  update.message.reply_text(text)

  # Wait for user's response
  selected_indices = context.bot.wait_for_message(check=lambda message: message.chat_id == update.message.chat_id).text.split()
  selected_tasks = [recommended_tasks[int(i)-1] for i in selected_indices if int(i) <= len(recommended_tasks)]
  selected_habits = [recommended_habits[int(i)-1-len(recommended_tasks)] for i in selected_indices if int(i) > len(recommended_tasks)]

  # Update the user's checklist with the selected tasks and habits
  user_checklist = user_database.get_user(user_email).checklist
  user_checklist.tasks.extend(selected_tasks)
  user_checklist.habits.extend(selected_habits)
