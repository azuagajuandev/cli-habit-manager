from models import HabitManager, Habit
import json

FILE_NAME = "habits.json"

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