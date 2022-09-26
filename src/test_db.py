import unittest
import sqlite3
from model import Habit,Streak
from typing import List
from db import createTableHabits,createTableStreaks, getAllHabits,insertHabit,insertStreak,deleteHabit,dropTables,completeHabit,periodicityLogic,change_position,getAllStreaks

conn = sqlite3.connect('test.db',detect_types=sqlite3.PARSE_DECLTYPES)
c2 = conn.cursor()

class TestDb(unittest.TestCase):


    def setUp(self):
        task = "habit1"
        periodicity = 1
        self.habit_1 = Habit(task,periodicity)
        
    
    def test_insertHabit(self):
        createTableHabits(c2)
        createTableStreaks(c2)
        insertHabit(self.habit_1,c2)
        listHabits = getAllHabits(c2)
        self.assertEqual(listHabits[0].task,"habit1")
        dropTables(c2)
    
    def test_insertStreak(self):
        createTableHabits(c2)
        createTableStreaks(c2)
        insertHabit(self.habit_1,c2)
        listHabits = getAllHabits(c2)
        insertStreak(listHabits[0],c2)
        listStreaks = getAllStreaks(c2)
        self.assertEqual(listHabits[0].position,listStreaks[0].position)
        dropTables(c2)
    
    def test_completeHabit(self):
        createTableHabits(c2)
        createTableStreaks(c2)
        insertHabit(self.habit_1,c2)
        completeHabit(0,c2)
        listHabits = getAllHabits(c2)
        self.assertEqual(listHabits[0].status,2)
        dropTables(c2)

    def test_deleteHabit(self):
        createTableHabits(c2)
        createTableStreaks(c2)
        insertHabit(self.habit_1,c2)
        deleteHabit(0,c2)
        listHabits = getAllHabits(c2)
        self.assertEqual(len(listHabits),0)
        dropTables(c2)
    
    
    def test_periodicityLogic(self):
        pass

    def getAllHabits(c) -> List[Habit]:
        c2.execute('select * from habits')
        results = c.fetchall()
        habits = []
        for result in results:
            habits.append(Habit(*result))
        return habits



    
    
if __name__ == '__main__':
    unittest.main()