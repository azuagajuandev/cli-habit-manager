class Habit:
    def __init__(self, id, name, frequency=None, done=False):
        self.id = id
        self.name = name
        self.frequency = frequency
        self.done = done
    
    def mark_done(self):
        self.done = True
    
    def __str__(self):
        if self.done:
            prefix = "[X]"
        else:
            prefix = "[ ]"
        
        if self.frequency is not None:
            frequency = f" {self.frequency}"
        else:
            frequency = ""
        
        return f"{prefix} {self.id} - {self.name}{frequency}"

class HabitManager:
    def __init__(self):
        self.habits = {}
        self.next_id = 1
    
    def add_habit(self, name, frequency=None):
        habit = Habit(self.next_id, name, frequency)
        self.habits[habit.id] = habit
        self.next_id += 1
        return habit
    
    def list_habits(self):
        return list(self.habits.values())


if __name__ == "__main__":
    manager = HabitManager()
    manager.add_habit("Read 10 minutes", "daily")
    manager.add_habit("Gym")

    habits = manager.list_habits()
    for habit in habits:
        print(habit)