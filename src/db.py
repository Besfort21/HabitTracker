import sqlite3
import datetime
from datetime import timedelta
from typing import List
from model import Habit,Streak

conn = sqlite3.connect('habits.db',detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()

def createTableHabits(c):
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

def createTableStreaks(c):
    c.execute("""CREATE TABLE IF NOT EXISTS streaks (
            streaks integer,
            position integer
            )""")
        
createTableHabits(c=c)
createTableStreaks(c=c)

def insertHabit(habit: Habit,c):
    c.execute('select count(*) FROM habits')
    count = c.fetchone()[0]
    habit.position = count if count else 0
    with conn:
        c.execute('INSERT INTO habits  VALUES (:task, :periodicity,:position,:dateAdded,:dateCompleted,:datePeriod,:status,:brokenHabits,:streaks)',
        {'task': habit.task, 'periodicity': habit.periodicity,'position':habit.position,'dateAdded': datetime.datetime.now(),'dateCompleted':None,
         'datePeriod':datetime.datetime.now() + timedelta(days=habit.periodicity),'status':1,'brokenHabits': 0,'streaks':0})

def insertStreak(habit:Habit,c):
    with conn:
        c.execute('INSERT INTO streaks VALUES(:streaks,:position)',
                  {'streaks':habit.streaks,'position':habit.position})

def getAllHabits(c) -> List[Habit]:
    periodicityLogic(c)
    c.execute('select * from habits')
    results = c.fetchall()
    habits = []
    for result in results:
        habits.append(Habit(*result))
    return habits
        
def getAllStreaks(c) -> List[Streak]:
    c.execute('select * from streaks')
    results = c.fetchall()
    streaks = []
    for result in results:
        streaks.append(Streak(*result))
    return streaks

def deleteHabit(position,c):
    c.execute('select count(*) from habits')
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE from habits WHERE position=:position", {"position": position})
        c.execute("DELETE from streaks WHERE position=:position", {"position": position})

        for pos in range(position+1, count):
            change_position(pos, pos-1, False,c=c)

def change_position(old_position: int, new_position: int,c, commit=True):
    c.execute('UPDATE habits SET position = :position_new WHERE position = :position_old',
                {'position_old': old_position, 'position_new': new_position})
    if commit:
        conn.commit()

def completeHabit(position,c):
    with conn:
        c.execute('UPDATE habits SET status =:status,dateCompleted = :dateCompleted  WHERE position =:position',
                    {'position': position,'dateCompleted':datetime.datetime.now(),'status':2})

def periodicityLogic(c):
    """
    Function Implementing the Periodicity Logic

    First select all habits and store them in a list.
    Then loop through the habits.
    If the current date is larger than the calculated datePeriod,actions depending on the habit status will be performed.
    But before that independed on the status the new datePeriod will be calculated and updated.

    If the habits is not completed status = 1, the streak counter will be saved in the streak table and then reseted.
    After that the status will be changed to broken habits status = 3 and the brokenhabits counter will be incremented by one.

    If the habit is completed the status will be changed to not Done, the dateCompleted will be set to None and the streak counter will be incremented by one.

    """
    c.execute('select * from habits')
    results = c.fetchall()
    habits = []
    for result in results:
        habits.append(Habit(*result))
    for habit in habits:
        with conn:
            if datetime.datetime.now() > habit.datePeriod:
                status = habit.status
                position = habit.position
                datePeriod = habit.datePeriod + datetime.timedelta(days=habit.periodicity)
                c.execute('UPDATE habits SET datePeriod = :datePeriod WHERE position = :position',{'position':position,'datePeriod':datePeriod})
                
                if status == 1:
                    brokenHabits = habit.brokenHabits
                    insertStreak(habit,c)
                    c.execute("UPDATE habits SET streaks = :streaks  WHERE position = :position",{"position":position,'streaks':0})
                    c.execute("UPDATE habits SET status = :status WHERE position = :position",{"position":position,'status':3})
                    c.execute("UPDATE habits SET brokenHabits = :brokenHabits  WHERE position = :position",{"position":position,'brokenHabits':brokenHabits+1})
                if status == 2:
                    streaks = habit.streaks
                    c.execute('UPDATE habits SET status = :status WHERE position = :position',{'position':position,'status':1})
                    c.execute('UPDATE habits SET dateCompleted = :dateCompleted WHERE position = :position',{'position':position,'dateCompleted':None})
                    c.execute("UPDATE habits SET streaks = :streaks  WHERE position = :position",{"position":position,'streaks':streaks+1})


def dropTables(c):
    c.execute('DROP table habits')
    c.execute('DROP table streaks')
#dropTables()