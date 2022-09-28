from model import Habit,Streak
from db import conn
from typing import List



c = conn.cursor()

def samePeriodicity() -> List[Habit]:
    c.execute("select * from habits ORDER BY periodicity DESC")
    results = c.fetchall()
    same = []
    for result in results:
        same.append(Habit(*result))
    return same

def maxStreakAll() -> List[Streak]:
    c.execute("select * from streaks WHERE streaks = (SELECT MAX(streaks) from streaks)")
    results = c.fetchall()
    max = []
    for result in results:
        max.append(Streak(*result))
    return max

def maxStreakAllCurrent() -> List[Habit]:
    c.execute("select * from habits WHERE streaks = (SELECT MAX(streaks) from habits)")
    results = c.fetchall()
    max = []
    for result in results:
        max.append(Habit(*result))
    return max

def maxStreakHabit(position) -> List[Streak]:
    position -= 1
    c.execute("select * from streaks WHERE position = :position and streaks = (SELECT MAX(streaks) from streaks)",{'position':position})
    results = c.fetchall()
    max = []
    for result in results:
        max.append(Streak(*result))
    return max


def mostStruggle() ->List[Habit]:
    c.execute("select * from habits ORDER BY brokenhabits DESC")
    results = c.fetchall()
    struggles = []
    for result in results:
        struggles.append(Habit(*result))
    return struggles