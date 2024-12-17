
import pyautogui
import time
import random
import keyboard  # For ESC key detection
import customtkinter as ctk
from tkinter import messagebox
import threading  # To run typing in a separate thread

stop_typing_flag = False  # Global flag to stop typing

# Typing Bot Function
def typing_bot(text, base_speed, typo_chance):
    global stop_typing_flag
    stop_typing_flag = False

    for char in text:
        if stop_typing_flag or keyboard.is_pressed("esc"):
            stop_typing_flag = True
            messagebox.showinfo("Typing Stopped", "ESC pressed. Typing stopped.")
            return

        # Randomized speed (offsets for realism)
        current_speed = base_speed + random.uniform(-0.03, 0.03)
        time.sleep(max(0.01, current_speed))

        # Introduce random typos
        if random.random() < typo_chance:
            typo = random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            pyautogui.typewrite(typo, interval=current_speed)
            time.sleep(0.2)  # Delay before fixing the typo
            pyautogui.press("backspace")
            time.sleep(0.1)

        # Type the actual character
        pyautogui.typewrite(char, interval=current_speed)

        # Add longer pauses after sentence-ending punctuation
        if char in ".!?":
            pause_time = random.uniform(0.5, 2.0)  # Random pause between 0.5 and 2 seconds
            time.sleep(pause_time)

# Start Typing Function
def start_typing():
    global stop_typing_flag
    text = text_input.get("1.0", "end-1c").strip()
    if not text:
        messagebox.showwarning("No Text", "Please enter some text to type!")
        return

    # Get typing speed and typo chance
    speed = 1 / speed_slider.get()
    typo_chance = typo_slider.get() / 100

    # Starting message
    messagebox.showinfo("Get Ready", "Place your cursor where you want to type. Starting in 3 seconds...")
    time.sleep(3)

    # Run typing in a separate thread
    threading.Thread(target=typing_bot, args=(text, speed, typo_chance), daemon=True).start()

# Exit Application
def exit_app():
    root.quit()

# GUI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Typing Bot")
root.geometry("500x500")
root.resizable(False, False)

# Title Label
title_label = ctk.CTkLabel(root, text="Typing Bot", font=("Helvetica", 24, "bold"))
title_label.pack(pady=10)

# Text Input Box
text_label = ctk.CTkLabel(root, text="Enter Text to Type:", anchor="w", font=("Helvetica", 14))
text_label.pack(padx=10, pady=(5, 0))

text_input = ctk.CTkTextbox(root, width=450, height=150, corner_radius=10)
text_input.pack(pady=10)

# Speed Slider
speed_label = ctk.CTkLabel(root, text="Typing Speed (chars/sec): 10", anchor="w")
speed_label.pack(padx=10, pady=(5, 0))

def update_speed_label(value):
    speed_label.configure(text=f"Typing Speed (chars/sec): {int(value)}")

speed_slider = ctk.CTkSlider(root, from_=2, to=30, number_of_steps=28, command=update_speed_label)
speed_slider.set(10)
speed_slider.pack(padx=10, pady=5)

# Typo Chance Slider
typo_label = ctk.CTkLabel(root, text="Typo Chance (%): 5", anchor="w")
typo_label.pack(padx=10, pady=(5, 0))

def update_typo_label(value):
    typo_label.configure(text=f"Typo Chance (%): {int(value)}")

typo_slider = ctk.CTkSlider(root, from_=0, to=20, number_of_steps=20, command=update_typo_label)
typo_slider.set(5)
typo_slider.pack(padx=10, pady=5)

# Buttons
button_frame = ctk.CTkFrame(root, corner_radius=10)
button_frame.pack(pady=20)

start_button = ctk.CTkButton(button_frame, text="Start Typing", command=start_typing, width=180)
start_button.grid(row=0, column=0, padx=10)

exit_button = ctk.CTkButton(button_frame, text="Exit", command=exit_app, fg_color="red", hover_color="#D14A4A", width=180)
exit_button.grid(row=0, column=1, padx=10)

# Info Label
info_label = ctk.CTkLabel(root, text="Press 'ESC' to stop typing at any time.", font=("Helvetica", 12), text_color="gray")
info_label.pack(pady=10)

# ESC Listener Thread
def esc_listener():
    global stop_typing_flag
    while True:
        if keyboard.is_pressed("esc"):
            stop_typing_flag = True
            break
        time.sleep(0.1)

threading.Thread(target=esc_listener, daemon=True).start()

# Run the Application
root.mainloop()
