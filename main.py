import turtle
from turtle import Turtle, Screen
import pandas as pd
IMAGE = "blank_states_img.gif"
FONT = ("Arial", 8, "normal")
ALIGN = "center"

df = pd.read_csv("50_states.csv")
df["has_been_guessed"] = 0


class StatePrinter(Turtle):

    def __init__(self):
        super(StatePrinter, self).__init__()
        self.hideturtle()
        self.penup()

    def print_state(self, user_guess):
        x = df.loc[df["state"] == user_guess].iloc[0].at["x"]
        y = df.loc[df["state"] == user_guess].iloc[0].at["y"]
        self.goto(x, y)
        self.write(f"{user_guess}", font=FONT, align=ALIGN)

    def print_score(self, usr_score):
        self.goto(0, 0)
        if usr_score == 50:
            self.write("Congratulations! You win!", font=("Arial", 20, "normal"), align=ALIGN)
        else:
            self.write(f"Your final score was {usr_score}/50", font=("Arial", 20, "normal"), align=ALIGN)


screen = Screen()
screen.setup(width=725, height=491)
screen.title("U.S. States Game")
sp = StatePrinter()

screen.addshape(IMAGE)
turtle.shape(IMAGE)

score = df["has_been_guessed"].sum()
while score < 50:
    guess = screen.textinput(title=f"{score}/50 states guessed", prompt="What's the name of another state?")

    if guess is None:
        sp.print_score(score)
        break

    else:
        guess = guess.title()

    if df["state"].str.fullmatch(guess).any():
        df.loc[df["state"] == guess, "has_been_guessed"] = 1
        sp.print_state(guess)

    score = df["has_been_guessed"].sum()
    if score == 50:
        sp.print_score(score)


missed_states = df.loc[df["has_been_guessed"] == 0]["state"]
missed_states.to_csv("states_to_learn.csv")

screen.exitonclick()
