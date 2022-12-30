# In main.py
import os

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import user_database
import checklist_database
import task_habit_database
import carryover
import select_tasks_habits
import end_of_weekday
import generate_daily_infographic
import generate_weekly_infographic
import multiple_choice_menu
import logout

# Dictionary to store the MultipleChoiceMenu object for each user
menu_dict = {}

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
  name, email, password = context.bot.wait_for_message(check=lambda message: message.chat_id == update.message.chat_id).text.split()
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
  email, password = context.bot.wait_for_message(check=lambda message: message.chat_id == update.message.chat_id).text.split()
  email = email.strip()
  password = password.strip()
  # Authenticate user
  if user_database.authenticate(email, password):
    update.message.reply_text("Login successful!")
  else:
    update.message.reply_text("Invalid email or password.")

def menu(update, context):
  # Get the user's chat ID
  chat_id = update.message.chat_id
  # Check if the user has a MultipleChoiceMenu object in the dictionary
  if chat_id in menu_dict:
    # Display the user's menu options
    menu = menu_dict[chat_id]
  else:
    # Create a new MultipleChoiceMenu object for the user and add it to the dictionary
    menu = multiple_choice_menu.MultipleChoiceMenu()
    menu_dict[chat_id] = menu
  # Display the menu options and handle the user's response
  menu.navigate(update, context, menu.root)


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
  # Get the user's chat ID
  chat_id = update.message.chat_id
  # Check if the user has a MultipleChoiceMenu object in the dictionary
  if chat_id in menu_dict:
    # Display the user's menu options
    menu_dict[chat_id].display_menu()
  else:
    # Create a new MultipleChoiceMenu object for the user and add it to the dictionary
    menu = multiple_choice_menu.MultipleChoiceMenu()
    menu_dict[chat_id] = menu
    # Display the user's menu options
    menu.display_menu(update, context)
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
    task_habit_database.add_task(name, description, priority)
  update.message.reply_text("Task or habit '{}' has been added successfully.".format(name))

def update_task_habit(update, context):
  # Prompt user to enter the name and new status of the task or habit they want to update
  update.message.reply_text("Please enter the name and new status of the task or habit you want to update, separated by a space. (Status should be 'completed' or 'incomplete'.)")
  # Wait for user's response
  name, status = context.bot.wait_for(
      'message', check=lambda message: message.chat_id == update.message.chat_id)
  name = name.strip()
  status = status.strip().lower()
  # Update task or habit in the database
  task_habit_database.update_task_habit(name, status)
  update.message.reply_text("Task or habit '{}' has been updated successfully.".format(name))

def delete_task_habit(update, context):
  # Get the user's chat ID
  chat_id = update.message.chat_id
  # Check if the user has a MultipleChoiceMenu object in the dictionary
  if chat_id in menu_dict:
    # Display the user's menu options
    menu_dict[chat_id].display_options()
  else:
    # Create a new MultipleChoiceMenu object for the user and add it to the dictionary
    menu = multiple_choice_menu.MultipleChoiceMenu()
    menu_dict[chat_id] = menu
    # Display the user's menu options
    menu.display_options()
  # Prompt user to enter the name of the task or habit they want to delete
  update.message.reply_text("Please enter the name of the task or habit you want to delete.")
  # Wait for user's response
  name = context.bot.wait_for(
      'message', check=lambda message: message.chat_id == update.message.chat_id)
  name = name.strip()
  # Delete task or habit from the database
  task_habit_database.delete_task_habit(name)
  update.message.reply_text("Task or habit '{}' has been deleted successfully.".format(name))

def carryover_checklist(update, context):
  # Carry over previous week's uncompleted checklist items
  carryover.carryover_checklist()
  update.message.reply_text("Previous week's uncompleted checklist items have been carried over.")

def select_task_habit_today(update, context):
  # Ask user to select a task or habit for today
  select_tasks_habits.select_task_habit_today()
  update.message.reply_text("Please select a task or habit for today from the list provided.")

def end_of_weekday(update, context):
  # Prompt user to update their list and review their progress
  end_of_weekday.end_of_weekday_prompt()
  update.message.reply_text("Please update your list and review your progress for the day.")

def generate_daily_infographic(update, context):
  # Generate and send personalized infographic summary of the user's progress through their checklist
  generate_daily_infographic.generate_daily_infographic()
  update.message.reply_text("Your personalized infographic summary for the day has been sent to your chat.")

def generate_weekly_infographic(update, context):
  # Generate and send more comprehensive personalized infographic summary of the user's progress towards accomplishing their weekly checklist
  generate_weekly_infographic.generate_weekly_infographic()
  update.message.reply_text("Your personalized infographic summary for the week has been sent to your chat.")

def logout(update, context):
  # Logout user from their account
  logout.logout()
  update.message.reply_text("You have been logged out of your account.")

def main():
  # Create Telegram bot and get updates
  updater = Updater(TOKEN, use_context=True)
  # Add command handlers
  updater.dispatcher.add_handler(CommandHandler('start', start))
  updater.dispatcher.add_handler(CommandHandler('create_account', create_account))
  updater.dispatcher.add_handler(CommandHandler('login', login))
  updater.dispatcher.add_handler(CommandHandler('menu', menu))
  updater.dispatcher.add_handler(CommandHandler('create_checklist', create_checklist))
  updater.dispatcher.add_handler(CommandHandler('create_task_habit', create_task_habit))
  updater.dispatcher.add_handler(CommandHandler('update_task_habit', update_task_habit))
  updater.dispatcher.add_handler(CommandHandler('delete_task_habit', delete_task_habit))
  updater.dispatcher.add_handler(CommandHandler('carryover_checklist', carryover_checklist))
  updater.dispatcher.add_handler(CommandHandler('carryover_tasks', carryover))
  updater.dispatcher.add_handler(CommandHandler('select_tasks_habits', select_tasks_habits))
  updater.dispatcher.add_handler(CommandHandler('end_of_weekday', end_of_weekday))
  updater.dispatcher.add_handler(CommandHandler('generate_daily_report', generate_daily_infographic))
  updater.dispatcher.add_handler(CommandHandler('generate_weekly_report', generate_weekly_infographic))
  updater.dispatcher.add_handler(CommandHandler('logout', logout))

  # Start the bot
  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()