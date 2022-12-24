import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import user_database
import checklist_database
import task_habit_database
import carryover
import select_task_habit
import end_of_weekday_prompt
import generate_daily_infographic
import generate_weekly_infographic
import multiple_choice_menu
import logout

def start(update, context):
  # Welcome message and instructions for using the chatbot
  update.message.reply_text("Welcome to the Motivational Coaching Chatbot! Here are some commands you can use:\n\n"
                            "/create_account - create a new account\n"
                            "/login - login to your account\n"
                            "/menu - access the main menu\n")

def create_account(update, context):
  # Prompt user to enter their name, email, and password
  update.message.reply_text("Please enter your name, email, and password, separated by spaces.")
  # Wait for user's response
  name, email, password = context.bot.wait_for(
      'message', check=lambda message: message.chat_id == update.message.chat_id)
  name = name.strip()
  email = email.strip()
  password = password.strip()
  # Add user to the database
  user_database.add_user(name, email, password)
  update.message.reply_text("Your account has been created successfully.")

def login(update, context):
  # Prompt user to enter their email and password
  update.message.reply_text("Please enter your email and password, separated by a space.")
  # Wait for user's response
  email, password = context.bot.wait_for(
      'message', check=lambda message: message.chat_id == update.message.chat_id)
  email = email.strip()
  password = password.strip()
  # Authenticate user
  if user_database.authenticate(email, password):
    update.message.reply_text("Login successful!")
  else:
    update.message.reply_text("Invalid email or password.")

def menu(update, context):
  # Display multiple choice menu options
  multiple_choice_menu.navigate(multiple_choice_menu.root)

def create_checklist(update, context):
  # Prompt user to enter the name and description of their checklist
  update.message.reply_text("Please enter the name and description of your checklist, separated by a space.")
  # Wait for user's response
  name, description = context.bot.wait_for(
      'message', check=lambda message: message.chat_id == update.message.chat_id)
  name = name.strip()
  description = description.strip()
  # Create new checklist and add it to the database
  checklist = checklist_database.Checklist(name, description)
  checklist_database.add_checklist(checklist)
  update.message.reply_text("Checklist '{}' has been created successfully.".format(name))


def create_task_habit(update, context):
  # Prompt user to enter the name, description, frequency, and priority of their task or habit
  update.message.reply_text("Please enter the name, description, frequency, and priority of your task or habit, separated by spaces. (Frequency should be 'daily' or 'weekly', priority should be a number from 1 to 5, with 1 being the highest priority.)")
  # Wait for user's response
  name, description, frequency, priority = context.bot.wait_for(
      'message', check=lambda message: message.chat_id == update.message.chat_id)
  name = name.strip()
  description = description.strip()
  frequency = frequency.strip().lower()
  priority = priority.strip()
  # Add task or habit to the database
  if frequency == 'daily':
    task_habit_database.add_habit(name, description, frequency, priority)
  elif frequency == 'weekly':
    task_habit_database.add_habit(name, description, frequency, priority)
  else:
    update.message.reply_text("Invalid frequency. Please enter 'daily' or 'weekly'.")

def carryover_tasks(update, context):
  # Carry over previous week's uncompleted tasks and habits
  checklist = checklist_database.get_current_checklist()
  carryover.carryover(checklist)
  update.message.reply_text("Previous week's uncompleted tasks and habits have been carried over.")

def select_tasks_habits(update, context):
  # Recommend tasks and habits based on past performance and user preferences
  checklist = checklist_database.get_current_checklist()
  past_performance = task_habit_database.get_past_performance()
  user_preferences = task_habit_database.get_user_preferences()
  recommended_tasks, recommended_habits = select_task_habit.select_task_habit(checklist, past_performance, user_preferences)
  update.message.reply_text("Here are some tasks and habits you might want to consider for today:\n\n"
                            "Tasks:\n" + '\n'.join([task.name for task in recommended_tasks]) + "\n\n"
                            "Habits:\n" + '\n'.join([habit.name for habit in recommended_habits]))

def end_of_weekday(update, context):
  # Predict likely tasks and habits that will be completed based on past performance
  checklist = checklist_database.get_current_checklist()
  past_performance = task_habit_database.get_past_performance()
  likely_completed_tasks = end_of_weekday_prompt.end_of_weekday_prompt(checklist, past_performance)
  update.message.reply_text("Based on your past performance, here are some tasks and habits you are likely to complete today:\n\n"
                            + '\n'.join([task.name for task in likely_completed_tasks]) + "\n\n"
                            "Would you like to review your progress?")

def generate_daily_report(update, context):
  # Generate personalized infographic summary of user's progress through their checklist
  checklist = checklist_database.get_current_checklist()
  infographic = generate_daily_infographic.generate_daily_infographic(checklist)
  update.message.reply_text("Here is a summary of your progress today:\n\n" + infographic)

def generate_weekly_report(update, context):
  # Generate more comprehensive personalized infographic summary of user's progress towards accomplishing their weekly checklist
  checklist = checklist_database.get_current_checklist()
  infographic = generate_weekly_infographic.generate_weekly_infographic(checklist)
  update.message.reply_text("Here is a summary of your progress this week:\n\n" + infographic)

def logout(update, context):
  # Logout user and clear their session
  user_database.logout()
  update.message.reply_text("You have been logged out successfully.")

def main():
  # Initialize bot and updater
  TOKEN = "YOUR_API_TOKEN"
  bot = telegram.Bot(token=TOKEN)
  updater = Updater(token=TOKEN, use_context=True)

  # Add command handlers
  updater.dispatcher.add_handler(CommandHandler('start', start))
  updater.dispatcher.add_handler(CommandHandler('create_account', create_account))
  updater.dispatcher.add_handler(CommandHandler('login', login))
  updater.dispatcher.add_handler(CommandHandler('menu', menu))
  updater.dispatcher.add_handler(CommandHandler('create_checklist', create_checklist))
  updater.dispatcher.add_handler(CommandHandler('create_task_habit', create_task_habit))
  updater.dispatcher.add_handler(CommandHandler('carryover_tasks', carryover_tasks))
  updater.dispatcher.add_handler(CommandHandler('select_tasks_habits', select_tasks_habits))
  updater.dispatcher.add_handler(CommandHandler('end_of_weekday', end_of_weekday))
  updater.dispatcher.add_handler(CommandHandler('generate_daily_report', generate_daily_report))
  updater.dispatcher.add_handler(CommandHandler('generate_weekly_report', generate_weekly_report))
  updater.dispatcher.add_handler(CommandHandler('logout', logout))

  # Start the bot
  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()
