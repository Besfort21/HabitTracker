import typer
from rich.console import Console
from rich.table import Table
from model import Habit,Streak
from db import insertHabit,getAllHabits,deleteHabit,completeHabit,getAllStreaks,conn
from analytics import maxStreakAll, maxStreakAllCurrent,maxStreakHabit,mostStruggle,samePeriodicity

console = Console()

app = typer.Typer()

c = conn.cursor()

#show all Habits / Main Table
@app.command(short_help='show all habits')
def show():
    habits = getAllHabits(c)
    console.print("[bold magenta]Habits[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Habit", min_width=20)
    table.add_column("Periodicity", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")
    table.add_column("Date added", min_width=20)
    table.add_column("DatePeriod", min_width=20)
    table.add_column("DateCompleted",min_width=20)
    is_done_str = ""
    periodicity_str = ""
    for idx, habit in enumerate(habits, start=1):

        if habit.status == 1:
            is_done_str = "Not Done"
        if habit.status == 2:
            is_done_str = "Done"
        if habit.status == 3:
            is_done_str = "Broken Habit"
        if habit.periodicity == 1:
            periodicity_str = "daily"
        if habit.periodicity == 7:
            periodicity_str = "weekly"

        table.add_row(str(idx), habit.task,periodicity_str, is_done_str,str(habit.dateAdded),str(habit.datePeriod),str(habit.dateCompleted))
    console.print(table)

#Table for Streaks.
@app.command(short_help='show all streaks')
def showStreaks():
    streaks = getAllStreaks(c)
    
    console.print("[bold magenta]Streaks[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Streaks", min_width=20)
    table.add_column('Habit Position',min_width=20)
    for streak in streaks:
        table.add_row(str(streak.streaks),str(streak.position+1))
    console.print(table)

#Table for the streaks of the habits currently shown in the main table.
@app.command(short_help='show current streaks')
def showCurrentStreaks():
    habits = getAllHabits(c)
    
    console.print("[bold magenta]Current Streaks[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Current Streak", min_width=20)
    table.add_column('Habit Position',min_width=20)
    for habit in habits:
        table.add_row(str(habit.streaks),str(habit.position+1))
    console.print(table)


@app.command(short_help='add an item with periodicity "daily" or "weekly" ')
def add(task: str, periodicity: str):
    """
    Function to be called when the user wants to add a habit.
    Creates a habit object.
    Calls the insertHabit function from the database module.
    Checks if the Input equals to either daily or weekly.

    Parameters:
    task (str): description of the habit.
    periodicity(str): describing wether a habit is a daily or weekly habit.
  
    """

    typer.echo(f"adding {task}, {periodicity}")
    if periodicity.lower() == "daily":
        periodicity = 1
    elif periodicity.lower() == "weekly":
        periodicity = 7
    else:
        raise ValueError("You need to enter either 'daily' or 'weekly' ")
        
    
    habit = Habit(task, periodicity)
    insertHabit(habit,c)
    show()


@app.command(short_help='delete an item')
def delete(position: int):
    """
    Function to be called when the user wants to delete a habit.

    Parameters:
    position: indicating the position of the habit to be deleted.
  
    """

    typer.echo(f"deleting {position}")
    # indices in Table begin at 1, but in database at 0
    deleteHabit(position-1,c)
    show()

@app.command(short_help='complete an item')
def complete(position: int):
    """
    Function to be called when the user wants to complete a habit.

    Parameters:
    position: indicating the position of the habit to be deleted.
  
    """

    typer.echo(f"complete {position}")
    completeHabit(position-1,c)
    show()

#Tables for the Analytics module ------------------------------

@app.command(short_help='show max streak')
def showMaxStreak():
    max = maxStreakAll()

    console.print("[bold magenta]Max Streak[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Max Streak", min_width=20)
    table.add_column('Habit Position',min_width=20)
    for i in max:
        table.add_row(str(i.streaks),str(i.position+1))
    console.print(table)

@app.command(short_help='show max streak')
def showCurrentMaxStreak():
    max = maxStreakAllCurrent()

    console.print("[bold magenta]Max Current Streak[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Max Streak", min_width=20)
    table.add_column('Habit Position',min_width=20)
    for i in max:
        table.add_row(str(i.streaks),str(i.position+1))
    console.print(table)

@app.command(short_help='show max Streak for given Habit')
def showMaxStreakHabit(position: int):
    max = maxStreakHabit(position)

    console.print("[bold magenta]Max Streak for Given Habit[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Max Streak", min_width=20)
    table.add_column('Habit Position',min_width=20)
    for i in max:
        table.add_row(str(i.streaks),str(i.position+1))
    console.print(table)

@app.command(short_help='show Habits with same Periodicity')
def showSamePeriodicity():
    same = samePeriodicity()

    console.print("[bold magenta]Habits[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Habit", min_width=20)
    table.add_column("Periodicity", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")
    table.add_column("Date added", min_width=20)
    table.add_column("DatePeriod", min_width=20)
    table.add_column("DateCompleted",min_width=20)
    is_done_str = ""
    periodicity_str = ""
    for idx, habit in enumerate(same, start=1):
        if habit.status == 1:
            is_done_str = "Not Done"
        if habit.status == 2:
            is_done_str = "Done"
        if habit.status == 3:
            is_done_str = "Broken Habit"
        if habit.periodicity == 1:
            periodicity_str = "daily"
        if habit.periodicity == 7:
            periodicity_str = "weekly"
        table.add_row(str(idx), habit.task,periodicity_str, is_done_str,str(habit.dateAdded),str(habit.datePeriod),str(habit.dateCompleted))
    console.print(table)

@app.command(short_help="Habits you have got most trouble with")
def showStruggle():
    struggles = mostStruggle()

    console.print("[bold magenta]Habits[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Habit", min_width=20)
    table.add_column("Periodicity", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")
    table.add_column("Date added", min_width=20)
    table.add_column("DatePeriod", min_width=20)
    table.add_column("DateCompleted",min_width=20)
    table.add_column("BrokenHabits",min_width=20)
    is_done_str = ""
    periodicity_str = ""
    for idx, habit in enumerate(struggles, start=1):
        if habit.status == 1:
            is_done_str = "Not Done"
        if habit.status == 2:
            is_done_str = "Done"
        if habit.status == 3:
            is_done_str = "Broken Habit"
        if habit.periodicity == 1:
            periodicity_str = "daily"
        if habit.periodicity == 7:
            periodicity_str = "weekly"
        table.add_row(str(idx), habit.task,periodicity_str, is_done_str,str(habit.dateAdded),str(habit.datePeriod),str(habit.dateCompleted),str(habit.brokenHabits))
    console.print(table)


if __name__ == "__main__":
    app()