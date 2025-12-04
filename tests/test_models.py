import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Habit, HabitManager

def test_habit_mark_done():
    h = Habit(1, "Read 10 minutes", "daily")
    assert h.done is False
    h.mark_done()
    assert h.done is True

def test_habit_str_shows_undone():
    h = Habit(1, "Read", "daily")
    text = str(h)
    assert "[ ]" in text
    assert "Read" in text
    assert "(daily)" in text

def test_add_and_list_habits():
    manager = HabitManager()
    h1 = manager.add_habit("Read", "daily")
    h2 = manager.add_habit("Gym")

    habits = manager.list_habits()
    assert len(habits) == 2
    assert habits[0].id == 1
    assert habits[1].id == 2