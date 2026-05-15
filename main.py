import tkinter as tk
import math
from textwrap import fill

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- GLOBAL VARIABLES ------------------------------- #
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, timer

    # Cancel the scheduled countdown if one exists
    if timer is not None:
        window.after_cancel(timer)

    # Reset timer display
    canvas.itemconfig(timer_text, text="00:00")

    # Reset title label
    mylabel.config(text="Timer", fg=GREEN)

    # Clear check marks
    check_marks.config(text="")

    # Reset repetition counter
    reps = 0
    timer = None


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # Every 8th rep -> long break
    if reps % 8 == 0:
        mylabel.config(text="Break", fg=RED)
        count_down(long_break_sec)

    # Every even rep -> short break
    elif reps % 2 == 0:
        mylabel.config(text="Break", fg=PINK)
        count_down(short_break_sec)

    # Odd reps -> work session
    else:
        mylabel.config(text="Timer", fg=GREEN)
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer

    count_min = math.floor(count / 60)
    count_sec = count % 60

    # Add leading zero to seconds if needed
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # Update timer text on canvas
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    # Continue countdown
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        # Start next session automatically
        start_timer()

        # Update check marks after each completed work session
        marks = ""
        work_sessions = math.floor(reps / 2)

        for _ in range(work_sessions):
            marks += "✔"

        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

mylabel = tk.Label(
    text="Timer",
    fg=GREEN,
    bg=YELLOW,
    font=(FONT_NAME, 35, "bold")
)
mylabel.grid(row=0, column=1)

canvas = tk.Canvas(
    window,
    width=200,
    height=224,
    bg=YELLOW,
    highlightthickness=0
)

tomato = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato)

timer_text = canvas.create_text(
    103,
    130,
    text="00:00",
    fill="white",
    font=(FONT_NAME, 35, "bold")
)

canvas.grid(column=1, row=1)

button_start = tk.Button(
    text="Start",
    highlightthickness=0,
    command=start_timer
)
button_start.grid(column=0, row=3)

button_reset = tk.Button(
    text="Reset",
    highlightthickness=0,
    command=reset_timer
)
button_reset.grid(column=2, row=3)

check_marks = tk.Label(
    text="",
    bg=YELLOW,
    fg=GREEN
)
check_marks.grid(column=1, row=3)

window.mainloop()