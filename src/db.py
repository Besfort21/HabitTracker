import sqlite3
import datetime
from datetime import timedelta
from typing import List
from model import Habit,Streak

conn = sqlite3.connect('habits.db',detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()

def createTableHabits():
    c.execute("""CREATE TABLE IF NOT EXISTS habits (
            task text,
            periodicity integer,
            position integer PRIMARY KEY,
            dateAdded timestamp,
            dateCompleted timestamp,
            datePeriod timestamp,
            status integer,
            brokenHabits integer,
            streaks integer
            )""")

def createTableStreaks():
    c.execute("""CREATE TABLE IF NOT EXISTS streaks (
            streaks integer,
            position integer
            )""")
        
createTableHabits()
createTableStreaks()

def insertHabit(habit: Habit):
    c.execute('select count(*) FROM habits')
    count = c.fetchone()[0]
    habit.position = count if count else 0
    with conn:
        c.execute('INSERT INTO habits  VALUES (:task, :periodicity,:position,:dateAdded,:dateCompleted,:datePeriod,:status,:brokenHabits,:streaks)',
        {'task': habit.task, 'periodicity': habit.periodicity,'position':habit.position,'dateAdded': datetime.datetime.now(),'dateCompleted':None,
         'datePeriod':datetime.datetime.now() + timedelta(days=habit.periodicity),'status':1,'brokenHabits': 0,'streaks':0})

def insertStreak(habit:Habit):
    with conn:
        c.execute('INSERT INTO streaks VALUES(:streaks,:position)',
                  {'streaks':habit.streaks,'position':habit.position})

def getAllHabits() -> List[Habit]:
    #periodicityLogic()
    c.execute('select * from habits')
    results = c.fetchall()
    habits = []
    for result in results:
        habits.append(Habit(*result))
    return habits
        
def getAllStreaks() -> List[Streak]:
    c.execute('select * from streaks')
    results = c.fetchall()
    streaks = []
    for result in results:
        streaks.append(Streak(*result))
    return streaks

def deleteHabit(position):
    c.execute('select count(*) from habits')
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE from habits WHERE position=:position", {"position": position})
        c.execute("DELETE from streaks WHERE position=:position", {"position": position})

        for pos in range(position+1, count):
            change_position(pos, pos-1, False)

def change_position(old_position: int, new_position: int, commit=True):
    c.execute('UPDATE habits SET position = :position_new WHERE position = :position_old',
                {'position_old': old_position, 'position_new': new_position})
    if commit:
        conn.commit()

def completeHabit(position):
    with conn:
        c.execute('UPDATE habits SET status =:status,dateCompleted = :dateCompleted  WHERE position =:position',
                    {'position': position,'dateCompleted':datetime.datetime.now(),'status':2})

#def periodicityLogic():

def dropTables():
    c.execute('DROP table habits')
    c.execute('DROP table streaks')
#dropTables()