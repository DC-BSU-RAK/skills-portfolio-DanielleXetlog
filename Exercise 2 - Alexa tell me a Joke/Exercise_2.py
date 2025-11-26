import tkinter as tk
from PIL import ImageTk, Image  #PIL and ImageTK handles images and displays on tkinter windows
import winsound  #Allows to play backgroud music on windows
import random  # Chooses random jokes from file
import os  # Handles text-to-speech

# Global variable for music state
music_playing = True

def play_background_music():
    # Plays the background music file in a continuous loop when called
    if music_playing:
        winsound.PlaySound("funny.wav", winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

def stop_background_music():
    # Stops any currently playing background music
    winsound.PlaySound(None, winsound.SND_PURGE)

def toggle_music():
    # Switches music between on and off states when mute button is clicked
    global music_playing
    music_playing = not music_playing
    if music_playing:
        play_background_music()
        mute_btn.config(text="🔊")
    else:
        stop_background_music()
        mute_btn.config(text="🔇")

def create_mute_button():
    # Creates the music toggle button that appears in top right corner of screen
    global mute_btn
    mute_btn = tk.Button(root, text="🔊", bg="#ba1717", fg="white",
                        relief="flat", borderwidth=0, font=("Arial", 16, "bold"),
                        activebackground="#ba1717", activeforeground="#f0b13d",
                        command=toggle_music)
    mute_btn.place(relx=0.94, rely=0.1, anchor="center")

def frame_one():
    # Main menu screen with START, INSTRUCTIONS, and QUIT buttons
    for widget in root.winfo_children():
        widget.destroy()
    
    # Load and display the main menu background image
    root.bg_image = ImageTk.PhotoImage(Image.open("Joke.png"))
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()
    canvas.create_image(0, 0, image=root.bg_image, anchor="nw")

    # Start playing background music when main menu loads
    play_background_music()
    
    # Add mute button to top right corner
    create_mute_button()

    # Create START button that leads to joke telling screen
    button = tk.Button(root, text="START", bg="#ba1717", fg="white",
    relief="flat", borderwidth=0, font=("Arial", 20, "bold"),
    activebackground="#ba1717", activeforeground="#f0b13d",
    command=frame_two)
    button.place(relx=0.5, rely=0.7, anchor="center")

    # Create INSTRUCTIONS button that shows game instructions
    button1 = tk.Button(root, text="INSTRUCTIONS", bg="#ba1717", fg="white",
    relief="flat", borderwidth=0, font=("Arial", 20, "bold"),
    activebackground="#ba1717", activeforeground="#f0b13d",
    command=frame_three)
    button1.place(relx=0.5, rely=0.79, anchor="center")

    # Create QUIT button that closes the application
    button2 = tk.Button(root, text="QUIT", bg="#ba1717", fg="white",
    relief="flat", borderwidth=0, font=("Arial", 20, "bold"),
    activebackground="#ba1717", activeforeground="#f0b13d",
    command=lambda: root.quit())
    button2.place(relx=0.5, rely=0.89, anchor="center")

def frame_two():
    # Joke telling screen where users can hear and see jokes
    for widget in root.winfo_children():
        widget.destroy()

    # Load and display the joke screen background image
    root.joke_bg = ImageTk.PhotoImage(Image.open("Jokes.png"))
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()
    canvas.create_image(0, 0, image=root.joke_bg, anchor="nw")
    
    # Add mute button to control music
    create_mute_button()
    
    # Display ALEXA title at top of joke area
    alexa_title = tk.Label(root, text="   ALEXA ", font=("Arial", 18, "bold"), bg="#c11d1d", fg="white")
    alexa_title.place(relx=0.5, rely=0.34, anchor="center")
    
    # Create label where joke text will be displayed
    joke_text = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#c11d1d", fg="white", wraplength=800)
    joke_text.place(relx=0.5, rely=0.5, anchor="center")
    
    current_joke = ""
    current_answer = ""
    
    def speak(text):
        # Uses Windows text-to-speech to read text aloud to user
        os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')
    
    def tell_joke():
        # Selects random joke from file and displays it on screen
        nonlocal current_joke, current_answer
        with open("punchlines.txt", "r") as file:
            lines = file.readlines()
            line = random.choice(lines).rstrip()
        if line:
            parts = line.split("?")
        if len(parts) == 2:
            current_joke = parts[0] + "?"
            current_answer = parts[1]
            # Show punchline first
            joke_text.config(text=current_joke)
            # Then read it after 100ms
            root.after(100, lambda: speak(current_joke))
    
    def show_answer():
        # Reveals the answer to current joke and plays sound effect
        joke_text.config(text=current_joke + "\n\n" + current_answer)
        root.after(100, lambda: speak(current_answer))
        # Stop background music and play sound effect
        root.after(500, lambda: [stop_background_music(), winsound.PlaySound("sound_effect1.wav", winsound.SND_FILENAME)])
        # Continue background music after sound effect
        root.after(2000, lambda: play_background_music())

    # BACK button returns user to main menu
    back_btn = tk.Button(root, text="BACK", bg="#ba1717", fg="white",
    relief="flat", borderwidth=0, font=("Arial", 18, "bold"),
    activebackground="#ba1717", activeforeground="#f0b13d",
    command=frame_one)
    back_btn.place(relx=0.15, rely=0.1, anchor="center")

    # ALEXA button tells a new joke when clicked
    alexa_btn = tk.Button(root, text="ALEXA TELL ME A JOKE", bg="#ba1717", fg="white",
    relief="flat", borderwidth=0, font=("Arial", 16, "bold"),
    activebackground="#ba1717", activeforeground="#f0b13d",
    command=tell_joke)
    alexa_btn.place(relx=0.5, rely=0.73, anchor="center")

    # SHOW ANSWER button reveals the punchline of current joke
    show_btn = tk.Button(root, text="SHOW JOKE ANSWER", bg="#ba1717", fg="white",
    relief="flat", borderwidth=0, font=("Arial", 16, "bold"),
    activebackground="#ba1717", activeforeground="#f0b13d",
    command=show_answer)
    show_btn.place(relx=0.5, rely=0.82, anchor="center")

    # NEXT JOKE button loads and displays a new random joke
    next_btn = tk.Button(root, text="NEXT JOKE", bg="#ba1717", fg="white",
    relief="flat", borderwidth=0, font=("Arial", 16, "bold"),
    activebackground="#ba1717", activeforeground="#f0b13d",
    command=tell_joke)
    next_btn.place(relx=0.5, rely=0.91, anchor="center")

def frame_three():
    # Instructions screen explaining how to use the application
    for widget in root.winfo_children():
        widget.destroy()
    
    # Load and display instructions background image
    root.instructions_bg = ImageTk.PhotoImage(Image.open("Instructions1.png"))
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()
    canvas.create_image(0, 0, image=root.instructions_bg, anchor="nw")
    
    # Add mute button to control music
    create_mute_button()
    
    # Display large INSTRUCTIONS title at top
    title = tk.Label(root, text="INSTRUCTIONS", font=("Arial", 50, "bold"), bg="#c11d1d", fg="white")
    title.place(relx=0.5, rely=0.40, anchor="center")
    
    # Welcome message introducing the game
    welcome_text = """Welcome to my Joke Time game and in this game you will be
    given 3 buttons to click on:"""
    welcome_label = tk.Label(root, text=welcome_text, font=("Arial", 14, "bold"), bg="#c11d1d", fg="white", justify="center")
    welcome_label.place(relx=0.5, rely=0.51, anchor="center")
    
    # Detailed instructions explaining what each button does
    instructions_text = """➧ There will be a punchline shown on the board and you will be clicking the 3 buttons which say:
- "Alexa tell me a Joke" which will show the punchline on the board.
- "Show joke answer" which will show the answer after.
- "Next joke" which will proceed to the next joke that you want to hear.

Good luck and have fun laughing!"""
    
    instructions_label = tk.Label(root, text=instructions_text, font=("Arial", 14), bg="#c11d1d", fg="white", justify="left")
    instructions_label.place(relx=0.5, rely=0.67, anchor="center")
    
    # BACK button returns user to main menu
    back_btn = tk.Button(root, text="BACK", bg="#ba1717", fg="white",
    relief="flat", borderwidth=0, font=("Arial", 18, "bold"),
    activebackground="#ba1717", activeforeground="#f0b13d",
    command=frame_one)
    back_btn.place(relx=0.15, rely=0.1, anchor="center")

# Create main application window with title and size
root = tk.Tk()
root.title("Exercise 2 - Alexa tell me a Joke")
root.geometry("1920x1080")
root.iconbitmap("Logo 2.ico")

# Start application by showing main menu screen
frame_one()

# Start the tkinter main event loop to run application
root.mainloop()