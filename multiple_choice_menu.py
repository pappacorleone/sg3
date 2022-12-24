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
      print(f"{i+1}. {option.text}")

  def navigate(self, node):
    while True:
      self.display_options(node.children)
      choice = input("Enter your choice: ")
      try:
        choice = int(choice)
        chosen_option = node.children[choice-1]
        if chosen_option.children:
          node = chosen_option
        else:
          chosen_option.action()
          break
      except ValueError:
        print("Invalid input. Please enter a valid number.")
      except IndexError:
        print("Invalid choice. Please enter a valid number.")
