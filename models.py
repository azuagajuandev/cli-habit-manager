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
            frequency = f" ({self.frequency})"
        else:
            frequency = ""
        
        return f"{prefix} {self.id} - {self.name}{frequency}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "frequency": self.frequency,
            "done": self.done
        }

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
    
    def mark_habit_done(self, habit_id):
        habit = self.habits.get(habit_id)

        if habit is None:
            return None

        habit.mark_done()

        return habit
    
    def remove_habit(self, habit_id):
        habit = self.habits.pop(habit_id, None)
        return habit
    
    def export_data(self):
        data = []
        
        for habit in self.list_habits():
            habit_dict = habit.to_dict()
            data.append(habit_dict)
        
        return data
    
    def import_data(self, data):
        self.habits = {}

        max_id = 0
        for habit_data in data:
            habit_id = habit_data["id"]
            name = habit_data["name"]
            frequency = habit_data["frequency"]
            done = habit_data["done"]
            habit = Habit(habit_id, name, frequency, done)
            self.habits[habit_id] = habit

            if habit_id > max_id:
                max_id = habit_id
        
        self.next_id = max_id + 1