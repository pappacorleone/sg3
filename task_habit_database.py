import heapq

class Task:
  def __init__(self, name, description, priority):
    self.name = name
    self.description = description
    self.priority = priority
    self.status = 'incomplete'

class Habit:
  def __init__(self, name, description, frequency):
    self.name = name
    self.description = description
    self.frequency = frequency
    self.status = 'incomplete'

class TaskHabitDatabase:
  def __init__(self):
    self.tasks = {}
    self.habits = {}

  def add_task(self, email, name, description, priority):
    task = Task(name, description, priority)
    if email in self.tasks:
      heapq.heappush(self.tasks[email], task)
    else:
      self.tasks[email] = [task]

  def update_task_status(self, email, task, status):
    task.status = status

  def delete_task(self, email, task):
    self.tasks[email].remove(task)

  def add_habit(self, email, name, description, frequency):
    habit = Habit(name, description, frequency)
    if email in self.habits:
      self.habits[email].append(habit)
    else:
      self.habits[email] = [habit]

  def update_habit_status(self, email, habit, status):
    habit.status = status

  def delete_habit(self, email, habit):
    self.habits[email].remove(habit)