import typer
from rich.console import Console
from rich.table import Table
from model import Habit,Streak
from db import insertHabit,getAllHabits,deleteHabit,completeHabit,getAllStreaks

console = Console()

app = typer.Typer()


@app.command(short_help='show all habits')
def show():
    habits = getAllHabits()
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


@app.command(short_help='show all streaks')
def showStreaks():
    streaks = getAllStreaks()
    
    console.print("[bold magenta]Streaks[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Streaks", min_width=20)
    table.add_column('Habit Position',min_width=20)
    for streak in streaks:
        table.add_row(str(streak.streaks),str(streak.position+1))
    console.print(table)


@app.command(short_help='add an item with periodicity "daily" or "weekly" ')
def add(task: str, periodicity: str):
    typer.echo(f"adding {task}, {periodicity}")
    if periodicity.lower() == "daily":
        periodicity = 1
    elif periodicity.lower() == "weekly":
        periodicity = 7
    habit = Habit(task, periodicity)
    insertHabit(habit)
    show()


@app.command(short_help='delete an item')
def delete(position: int):
    typer.echo(f"deleting {position}")
    # indices in UI begin at 1, but in database at 0
    deleteHabit(position-1)
    show()

@app.command(short_help='complete an item')
def complete(position: int):
    typer.echo(f"complete {position}")
    completeHabit(position-1)
    show()






if __name__ == "__main__":
    app()