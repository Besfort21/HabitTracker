from model import Habit,Streak
from db import conn
from typing import List



c = conn.cursor()

def samePeriodicity() -> List[Habit]:
    """
    Shows habits with same Periodicity.
  
    Sorts the habits by Periodicity in descending order.
  
    Parameters:
    None
  
    Returns:
    Habit: List of the sorted Habits
  
    """

    c.execute("select * from habits ORDER BY periodicity DESC")
    results = c.fetchall()
    same = []
    for result in results:
        same.append(Habit(*result))
    return same

def maxStreakAll() -> List[Streak]:
    """
    Shows the max Streak from the streaks table.
  
    Parameters:
    None
  
    Returns:
    Streak: Returns the list of the max Streaks.
  
    """
    
    c.execute("select * from streaks WHERE streaks = (SELECT MAX(streaks) from streaks)")
    results = c.fetchall()
    max = []
    for result in results:
        max.append(Streak(*result))
    return max

def maxStreakAllCurrent() -> List[Habit]:
    """
    Shows max Streak from the current Habits shown in the show table.
  
    Parameters:
    None
  
    Returns:
    Habit: List of the Habits with the max Streaks
  
    """

    c.execute("select * from habits WHERE streaks = (SELECT MAX(streaks) from habits)")
    results = c.fetchall()
    max = []
    for result in results:
        max.append(Habit(*result))
    return max

def maxStreakHabit(position) -> List[Streak]:
    """
    Shows max Streak for a specified habit from the streak table.
  
    Parameters:
    position: position of the habit in the show table.
  
    Returns:
    Streak: List of the max Streaks.
  
    """

    position -= 1
    c.execute("select * from streaks WHERE position = :position and streaks = (SELECT MAX(streaks) from streaks)",{'position':position})
    results = c.fetchall()
    max = []
    for result in results:
        max.append(Streak(*result))
    return max


def mostStruggle() ->List[Habit]:
    """
    Shows habits with same counter of brokenHabits.
  
    Sorts the habits by brokenhabits in descending order.
  
    Parameters:
    None
  
    Returns:
    Habit: List of the sorted Habits
  
    """

    c.execute("select * from habits ORDER BY brokenhabits DESC")
    results = c.fetchall()
    struggles = []
    for result in results:
        struggles.append(Habit(*result))
    return struggles