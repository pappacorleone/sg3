
from telegram import Update


class MenuOption:
  def __init__(self, text, children=None, action=None):
    self.text = text
    self.children = children
    self.action = action

class MultipleChoiceMenu:
  def __init__(self, root):
    self.root = root

  def display_options(self, options):
    for i, option in enumerate(options):
      text += f"{i+1}. {option.text}\n"
    return text

  def navigate(self, update, context, node):
    while True:
      # Display the menu options and get the user's response
      options = self.display_options(node.children)
      update.message.reply_text(options)
      response = context.bot.wait_for_message(
          check=lambda message: message.chat_id == update.message.chat_id)
      try:
        # Convert the user's response to an integer
        choice = int(response.text)
        chosen_option = node.children[choice-1]
        if chosen_option.children:
          # If the chosen option has children, navigate to the next menu level
          node = chosen_option
        else:
          # If the chosen option doesn't have children, execute the action
          chosen_option.action()
          break
      except ValueError:
        update.message.reply_text("Invalid input. Please enter a valid number.")
      except IndexError:
        update.message.reply_text("Invalid choice. Please enter a valid number.")
    
