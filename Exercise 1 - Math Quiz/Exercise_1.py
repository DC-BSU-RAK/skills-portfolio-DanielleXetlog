import tkinter as tk
from PIL import ImageTk, Image #PIL and ImageTK handles images and displays on tkinter windows
import winsound #Allows to play backgroud music on windows
import threading #Allows to run multiple task simuntaneously
import random #Generates random math equations.

def show_frame(frame): frame.tkraise()

def play_music_loop(): #Plays the background music in loop
    while music_playing:
        winsound.PlaySound("bg_music.wav", winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        break

def toggle_music(): #Toggle the music on/off
    global music_playing
    if music_playing:
        winsound.PlaySound(None, winsound.SND_PURGE)
        for btn in music_buttons: btn.config(text="🔇")
        music_playing = False
    else:
        music_playing = True
        threading.Thread(target=play_music_loop, daemon=True).start()
        for btn in music_buttons: btn.config(text="🔊")

def displayMenu(): show_frame(diff) #Shows the difficulty selection screen

def randomInt(difficulty): #Generates the random equation based on the difficulty level
    if difficulty == "easy": return random.randint(1, 9)
    elif difficulty == "moderate": return random.randint(10, 99)
    else: return random.randint(1000, 9999)

def decideOperation(): return random.choice(['+', '-']) #Randomly choosing between addition and subtraction

def displayProblem(num1, num2, operation): #Displays the math problem on the screen
    question_label.config(text=f"{num1} {operation} {num2} = ?")
    answer_entry.delete(0, tk.END) #Clears the previous answer
    feedback_label.config(text="") #Clears the feedback
    submit_button.config(state=tk.NORMAL) #Enable the submit button

def isCorrect(user_answer, correct_answer): #This checks if the users answer is correct and updates the score
    global attempts, score
    attempts += 1
    if user_answer == correct_answer:
        points = 10 if attempts == 1 else 5 #10 points if first try and 5 for second try
        score += points
        feedback_label.config(text=f"Correct! +{points} points", fg="#7ad200") 
        update_score()
        submit_button.config(state=tk.DISABLED)
        root.after(1500, next_question) #Timer (1.5 secs) before it moves to the next question
        return True
    else:
        if attempts == 1:
            feedback_label.config(text="Wrong! Try again", fg="#ff0000")
        else:
            feedback_label.config(text=f"Wrong! Answer: {correct_answer}", fg="red")
            submit_button.config(state=tk.DISABLED)
            root.after(1500, next_question)
        return False

def displayResults(): #Grading system which will be shown on the result screen
    final_score_label.config(text=f"FINAL SCORE\n{score}/100")
    if score >= 90: grade = "A+"
    elif score >= 80: grade = "A"
    elif score >= 70: grade = "B"
    elif score >= 60: grade = "C"
    elif score >= 50: grade = "D"
    else: grade = "F"
    grade_label.config(text=grade, fg="#ffe08c")
    show_frame(complete)

def start_quiz(difficulty): #This begins the game when selecting the difficulty
    global score, current_question, attempts, current_difficulty
    score = 0
    current_question = 1
    attempts = 0
    current_difficulty = difficulty
    update_score()
    update_counter()
    generate_question()
    show_frame(quiz)

def generate_question(): #This generates random math questions
    global correct_answer, attempts
    attempts = 0
    num1 = randomInt(current_difficulty)
    num2 = randomInt(current_difficulty)
    operation = decideOperation()
    correct_answer = num1 + num2 if operation == '+' else num1 - num2
    displayProblem(num1, num2, operation)

def check_answer(): #Checks the users answer
    try: user_answer = int(answer_entry.get())
    except: 
        feedback_label.config(text="Please enter a number!")
        return
    isCorrect(user_answer, correct_answer)

def next_question(): #Moves to the next question or shows the result when the quiz is completed
    global current_question
    if current_question < 10:
        current_question += 1
        update_counter()
        generate_question()
    else: displayResults()

def update_counter(): question_counter.config(text=f"{current_question:02d} - 10") #Updates the question progress counter
def update_score(): score_label.config(text=f"Score: {score}") #Updates the score displayed
def exit_quiz(): show_frame(home) #This returns to the home screen

# Initialize variables
music_playing = score = attempts = correct_answer = 0
current_question = 1
current_difficulty = "easy"
root = tk.Tk()
root.title("Exercise 1 - Mathematics")
root.geometry("1920x1080")
root.iconbitmap("Logo 1.ico")

# Create frames
home = tk.Frame(root); diff = tk.Frame(root); instruct = tk.Frame(root)
quiz = tk.Frame(root); complete = tk.Frame(root)
for frame in (home, diff, instruct, quiz, complete):
    frame.place(x=0, y=0, relwidth=1, relheight=1)

# Background images
home_bg = ImageTk.PhotoImage(Image.open("Mathematics.png"))
diff_bg = ImageTk.PhotoImage(Image.open("Difficulty.png"))
instruct_bg = ImageTk.PhotoImage(Image.open("Instructions.png"))
quiz_bg = ImageTk.PhotoImage(Image.open("Questions.png"))
complete_bg = ImageTk.PhotoImage(Image.open("Result.png"))

tk.Label(home, image=home_bg).place(x=0, y=0, relwidth=1, relheight=1)
tk.Label(diff, image=diff_bg).place(x=0, y=0, relwidth=1, relheight=1)
tk.Label(instruct, image=instruct_bg).place(x=0, y=0, relwidth=1, relheight=1)
tk.Label(quiz, image=quiz_bg).place(x=0, y=0, relwidth=1, relheight=1)
tk.Label(complete, image=complete_bg).place(x=0, y=0, relwidth=1, relheight=1)

# Music buttons
music_buttons = []
for frame in (home, diff, instruct, quiz, complete):
    btn = tk.Button(frame, text="🔇", font=("Arial", 17), bg='#46abe8', fg='white',
    activebackground='#46abe8', relief="flat", borderwidth=0, command=toggle_music)
    btn.place(relx=0.95, rely=0.05, anchor='center')
    music_buttons.append(btn)

# Home frame
tk.Label(home, text="MATHEMATICS QUIZ", font=("Arial", 70, "bold"), bg='#46abe8', fg='white').place(relx=0.5, rely=0.29, anchor='center')
tk.Label(home, text="Created by: Danielle Gatan", font=("Arial", 25), bg='#46abe8', fg='white').place(relx=0.5, rely=0.37, anchor='center')
for i, (text, cmd) in enumerate([("DIFFICULTY", displayMenu), ("INSTRUCTIONS", lambda: show_frame(instruct)), ("EXIT", root.destroy)]):
    tk.Button(home, text=text, font=("Arial", 20), bg='#90b45e', fg='white',
    activebackground='#90b45e', relief="flat", borderwidth=0, command=cmd).place(relx=0.5, rely=0.6+i*0.1, anchor='center')

# Difficulty frame
tk.Label(diff, text="SELECT DIFFICULTY", font=("Arial", 60, "bold"), bg='white', fg='#249be4').place(relx=0.5, rely=0.3, anchor='center')
tk.Label(diff, text="Choose your difficulty to start the game.", font=("Arial", 20), bg='white', fg='#249be4').place(relx=0.5, rely=0.4, anchor='center')
tk.Button(diff, text="back", font=("Arial", 20), bg='#46abe8', fg='white',
    activebackground='#46abe8', relief="flat", borderwidth=0, command=lambda: show_frame(home)).place(relx=0.3, rely=0.1, anchor='center')
for i, (text, diff_level) in enumerate([("EASY", "easy"), ("MODERATE", "moderate"), ("ADVANCED", "advanced")]):
    colors = ['#90b45e','#f9e105','#cd1f1f']
    tk.Button(diff, text=text, font=("Arial", 20), bg=colors[i], fg='white',
    activebackground=colors[i], relief="flat", borderwidth=0, command=lambda d=diff_level: start_quiz(d)).place(relx=0.5, rely=0.5+i*0.1, anchor='center')

# Instructions frame
tk.Label(instruct, text="INSTRUCTIONS", font=("Arial", 60, "bold"), bg='white', fg='#249be4').place(relx=0.6, rely=0.2, anchor='center')
tk.Label(instruct, text="\nWelcome to my Mathematics Quiz game\nand in this game you will be given 3 difficulties to choose:", font=("Arial", 12, "bold"), bg='white', fg='#249be4').place(relx=0.6, rely=0.3, anchor='center')
instructions_text = """
➧ Each difficulty will consist 10 questions for you to answer.
➧ You will be getting to choose which difficulty level you want to try:
    - EASY: Single-digits numbers (ex: 9 - 1 = ?)
    - MODERATE: Double-digit numbers (ex: 32 + 35 = ?)
    - ADVANCED: Four-digit numbers (ex: 7084 - 2534 = ?)

When answering the questions given you will have TWO chances to answer
each question.
➧ Scoring system:
    - 10 points is when you answered the question on your first try.
    - 5 points is when you got the answer corrected on your second try.
    - 0 points is when you didn't get answer correct on your two chances, when
    getting it wrong you will automatically move on to the next question.
➧ This mathematics quiz game only contains addition and subtraction only.
➧ Try to get the highest score possible at the end of the quiz

Good luck and have fun learning math!
"""
tk.Label(instruct, text=instructions_text, font=("Arial", 12), bg='white', fg='#249be4', justify='left').place(relx=0.6, rely=0.6, anchor='center')
tk.Button(instruct, text="back", font=("Arial", 20), bg='#46abe8', fg='white',
    activebackground='#46abe8', relief="flat", borderwidth=0, command=lambda: show_frame(home)).place(relx=0.3, rely=0.1, anchor='center')

# Quiz frame
score_label = tk.Label(quiz, text="Score: 0", font=("Arial", 20, "bold"), bg='#3aa3e3', fg='white')
score_label.place(relx=0.1, rely=0.05, anchor='center')
tk.Label(quiz, text="QUESTION", font=("Arial", 30, "bold"), bg='#a1dbff', fg='white').place(relx=0.5, rely=0.2, anchor='center')
question_label = tk.Label(quiz, text="", font=("Arial", 80, "bold"), bg='#a1dbff', fg='white')
question_label.place(relx=0.5, rely=0.4, anchor='center')
answer_entry = tk.Entry(quiz, font=("Arial", 30), justify='center', width=15, relief="flat", borderwidth=0)
answer_entry.place(relx=0.5, rely=0.57, anchor='center')
feedback_label = tk.Label(quiz, text="", font=("Arial", 20), bg='#a1dbff')
feedback_label.place(relx=0.5, rely=0.28, anchor='center')
submit_button = tk.Button(quiz, text="SUBMIT", font=("Arial", 25), bg='#90b45e', fg='white',
    activebackground='#90b45e', relief="flat", borderwidth=0, command=check_answer)
submit_button.place(relx=0.34, rely=0.86, anchor='center')
tk.Button(quiz, text="EXIT QUIZ", font=("Arial", 25), bg='#cd1f1f', fg='white',
    activebackground='#cd1f1f', relief="flat", borderwidth=0, command=exit_quiz).place(relx=0.66, rely=0.86, anchor='center')
question_counter = tk.Label(quiz, text="01 - 10", font=("Arial", 25, "bold"), bg='#a1dbff', fg='white')
question_counter.place(relx=0.5, rely=0.8, anchor='center')

# Complete frame
tk.Label(complete, text="RESULTS", font=("Arial", 60, "bold"), bg='#fffbd2', fg='#249be4').place(relx=0.5, rely=0.3, anchor='center')
final_score_label = tk.Label(complete, text="FINAL SCORE\n0/100", font=("Arial", 50), bg='#fffbd2', fg='#249be4', justify='left')
final_score_label.place(relx=0.37, rely=0.54, anchor='center')
grade_label = tk.Label(complete, text="", font=("Arial", 70, "bold"), bg='#ffb650', fg='#ffe08c')
grade_label.place(relx=0.69, rely=0.55, anchor='center')
tk.Button(complete, text="PLAY AGAIN", font=("Arial", 20), bg='#90b45e', fg='white',
    activebackground='#90b45e', relief="flat", borderwidth=0, command=displayMenu).place(relx=0.33, rely=0.8, anchor='center')
tk.Button(complete, text="BACK TO HOME", font=("Arial", 20), bg='#90b45e', fg='white',
    activebackground='#90b45e', relief="flat", borderwidth=0, command=lambda: show_frame(home)).place(relx=0.67, rely=0.8, anchor='center')

show_frame(home) #Starts the math quiz on the home screen
root.mainloop()