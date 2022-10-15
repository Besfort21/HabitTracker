import unittest
import sqlite3
import datetime
from datetime import timedelta
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
        """
        For testing in more detail one must run this test in isolation as this requires the data to stay for n days in the tables,
        but the other tests drop the tables after completion.
        """
        createTableHabits(c2)
        createTableStreaks(c2)
        insertHabit(self.habit_1,c2)
        #streaks = self.habit_1.streaks
        #brokenhabits = self.habit_1.brokenhabits
        listHabits = getAllHabits(c2)
        self.assertEqual(listHabits[0].status,1)

        #Testing if the habit is broken and updated streaks if habit did not meet the completion date.
        #self.assertEqual(listHabits[0].status,3)
        #self.assertEqual(listHabits[0].streaks,0)

        #Testing streak computation,dateCompleted and status if habit did meet the completion date
        #self.assertEqual(listHabits[0].streaks,streaks+1)
        #self.assertEqual(listHabits[0].status,1)
        #self.assertEqual(listHabits[0].dateCompleted,None)

        #Testing brokenhabits computation if habit did not meet the completion date.
        #self.assertEqual(listHabits[0].brokenhabits,brokenhabits+1)   

        dropTables(c2)

    def getAllHabits(c) -> List[Habit]:
        periodicityLogic(c=c2)
        c2.execute('select * from habits')
        results = c.fetchall()
        habits = []
        for result in results:
            habits.append(Habit(*result))
        return habits

    def periodicityLogic(c):

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




    
    
if __name__ == '__main__':
    unittest.main()