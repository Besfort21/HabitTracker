class Habit:
    """
    Class for the habits stored in the database.
    task and periodicity must be specified when creating a habit object.
  
    """
    
    def __init__(self,task,periodicity,position=None,dateAdded=None,dateCompleted=None,datePeriod=None,status=None,brokenHabits=None,streaks=None):
        self.task = task
        self.periodicity = periodicity
        self.position = position if position is not None else None
        self.dateAdded = dateAdded if dateAdded is not None else None
        self.dateCompleted = dateCompleted if dateCompleted is not None else None
        self.datePeriod = datePeriod if datePeriod is not None else None
        self.status = status if status is not None else None
        self.brokenHabits = brokenHabits if brokenHabits is not None else None
        self.streaks = streaks if streaks is not None else None

class Streak:
    """
    Class for the streaks stored in the database.
    User wont directly create a Streak object.This object will be created,
    when a habit did not meet the date for completion and therefore its current streak gets stored in the streak table
  
    """
    
    def __init__(self,streaks,position):
        self.streaks= streaks
        self.position = position