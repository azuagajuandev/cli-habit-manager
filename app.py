import json

FILE_NAME = "habits.json"

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

def cmd_add(manager, args):
    if not args:
        print("Name is required")
        return
    
    if len(args) == 1:
        name = args[0]
        frequency = None
    else:
        frequency = args[-1]
        name_words = args[:-1]
        name = " ".join(name_words)
    
    habit = manager.add_habit(name, frequency)
    print(habit)

def cmd_list(manager, args):
    if args:
        print("Args are not needed")
        return

    habits = manager.list_habits()

    for habit in habits:
        print(habit)

def cmd_done(manager, args):
    if not args:
        print("Habit id is needed")
        return

    raw_id = args[0]
    try:
        habit_id = int(raw_id)
    except ValueError:
        print("Habit id must be a number")
        return
    
    updated_habit = manager.mark_habit_done(habit_id)

    if updated_habit is None:
        print("Habit not found")
    else:
        print(updated_habit)

def cmd_remove(manager, args):
    if not args:
        print("Habit id is needed")
        return
    
    raw_id = args[0]
    try:
        habit_id = int(raw_id)
    except ValueError:
        print("Habit id must be a number")
        return
    
    removed_habit = manager.remove_habit(habit_id)

    if removed_habit is None:
        print("Habit not found")
    else:
        print("Removed", removed_habit)

def cmd_commands(_manager, args):
    if args:
        print("Args are not needed")
        return

    for command in commands:
        print(command)

def cmd_save(manager, args):
    if args:
        print("Args are not needed")
        return
    
    data = manager.export_data()
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("Habits saved")

def cmd_load(manager, args):
    if args:
        print("Args are not needed")
        return
    
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            data = json.load(f)
        manager.import_data(data)
        print("Habits loaded")
    except FileNotFoundError:
        print("No saved habits found")

commands = {
    "add": cmd_add,
    "list": cmd_list,
    "done": cmd_done,
    "remove": cmd_remove,
    "save": cmd_save,
    "load": cmd_load,
    "commands": cmd_commands,
    "help": cmd_commands,
}

if __name__ == "__main__":
    manager = HabitManager()

    while True:
        line = input("> ")
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd in ("quit", "exit"):
            print("Bye")
            break

        if cmd not in commands:
            print("Unknown command")
            continue

        handler = commands[cmd]
        handler(manager, args)