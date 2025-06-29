# Mental Health Mood Tracker with GUI and Mood Suggestions (Inside Out Edition)

import tkinter as tk
from tkinter import messagebox, Text, Toplevel, Label
from datetime import datetime
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os

# Download VADER lexicon if not already
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# =====================
# Data Setup
# =====================
data_file = "mood_journal.csv"
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=['Date', 'Text', 'Mood_Label', 'Suggestion'])
    df.to_csv(data_file, index=False)
else:
    df = pd.read_csv(data_file)

# =====================
# Mood Interpretation based on compound score with 9 moods
# =====================
def get_mood_details(score):
    if score >= 0.6:
        return ("Joy", "You’re radiating happiness! Share your light with others today.")
    elif 0.2 <= score < 0.6:
        return ("Envy", "You might be comparing yourself to others. Focus on your own growth 🌱")
    elif 0.05 <= score < 0.2:
        return ("Embarrassment", "Everyone makes mistakes. Be kind to yourself and move forward ❤️")
    elif -0.05 <= score < 0.05:
        return ("Boredom", "Things feel dull? Try doing something new or creative today 🎨")
    elif -0.2 <= score < -0.05:
        return ("Anxiety", "You seem tense. Take a deep breath and slow down 💆")
    elif -0.4 <= score < -0.2:
        return ("Fear", "Something’s worrying you. Talk it out with someone you trust 🫂")
    elif -0.6 <= score < -0.4:
        return ("Disgust", "You're put off by something. Take a moment to understand why and reset 🧼")
    elif -0.8 <= score < -0.6:
        return ("Sadness", "It’s okay to feel down. Let yourself rest and recharge 🛌")
    else:
        return ("Anger", "Strong feelings today. Channel them into something constructive 💪")

# =====================
# Save Entry Function
# =====================
def analyze_and_save():
    text = journal_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Empty Entry", "Please write something about your day.")
        return

    score = sia.polarity_scores(text)['compound']
    label, suggestion = get_mood_details(score)
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_entry = pd.DataFrame([[today, text, label, suggestion]],
                              columns=['Date', 'Text', 'Mood_Label', 'Suggestion'])
    global df
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(data_file, index=False)

    mood_output.config(state='normal')
    suggestion_output.config(state='normal')
    mood_output.delete("1.0", tk.END)
    suggestion_output.delete("1.0", tk.END)
    mood_output.insert(tk.END, label)
    suggestion_output.insert(tk.END, suggestion)
    mood_output.config(state='disabled')
    suggestion_output.config(state='disabled')

# =====================
# How to Use Window
# =====================
def show_instructions():
    how_to = Toplevel(root)
    how_to.title("How to Use")
    how_to.geometry("400x250")
    instructions = (
        "Welcome to the Mental Health Mood Tracker!\n\n"
        "1. Write about your thoughts or feelings in the journal box.\n"
        "2. Click the 'Mood analysis' button.\n"
        "3. Your mood and a suggestion will appear on the right.\n"
        "4. Your entries are automatically saved with time and analysis.\n\n"
        "Use it daily to reflect and track how you're doing."
    )
    Label(how_to, text=instructions, wraplength=380, justify='left', padx=10, pady=10).pack()

# =====================
# GUI Setup
# =====================
root = tk.Tk()
root.title("Mental Health Mood Tracker")
root.geometry("800x450")
root.configure(bg="white")

# Left side: Journal input
journal_label = tk.Label(root, text="Put your journal here:", font=("Helvetica", 12), bg="white")
journal_label.place(x=20, y=10)

journal_entry = Text(root, height=15, width=45, wrap='word', font=("Helvetica", 12), bd=2, relief='groove')
journal_entry.place(x=20, y=40)

# Right side: Mood analysis
analyze_btn = tk.Button(root, text="Mood analysis", command=analyze_and_save,
                        font=("Helvetica", 12, "bold"), bg="#4caf50", fg="white", padx=10, pady=5)
analyze_btn.place(x=550, y=20)

mood_label = tk.Label(root, text="Mood:", font=("Helvetica", 11), bg="white")
mood_label.place(x=500, y=80)

mood_output = Text(root, height=2, width=30, font=("Helvetica", 11), bg="#e0e0e0")
mood_output.place(x=500, y=105)
mood_output.config(state='disabled')

suggestion_label = tk.Label(root, text="Suggestion:", font=("Helvetica", 11), bg="white")
suggestion_label.place(x=500, y=170)

suggestion_output = Text(root, height=5, width=30, font=("Helvetica", 11), bg="#e0e0e0")
suggestion_output.place(x=500, y=195)
suggestion_output.config(state='disabled')

# Bottom help button
howto_btn = tk.Button(root, text="How to use", command=show_instructions,
                      font=("Helvetica", 10), bg="white", relief='solid')
howto_btn.place(x=360, y=400)

root.mainloop()