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
    self.tasks = []
    self.habits = []

  def add_task(self, name, description, priority):
    task = Task(name, description, priority)
    heapq.heappush(self.tasks, task)

  def update_task_status(self, task, status):
    task.status = status

  def delete_task(self, task):
    self.tasks.remove(task)

  def add_habit(self, name, description, frequency):
    habit = Habit(name, description, frequency)
    self.habits.append(habit)

  def update_habit_status(self, habit, status):
    habit.status = status

  def delete_habit(self, habit):
    self.habits.remove(habit)
