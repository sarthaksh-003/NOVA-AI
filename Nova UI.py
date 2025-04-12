import sys
import pyttsx3
import speech_recognition as sr
import pyautogui
import time
import os
import datetime
import wikipedia
import webbrowser
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import requests
import json
from bs4 import BeautifulSoup
import openai
import smtplib
from PIL import Image, ImageTk

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 150)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        log_text.insert(tk.END, "🎙 Listening...\n")
        try:
            audio = recognizer.listen(source)
            query = recognizer.recognize_google(audio, language='en-in')
            log_text.insert(tk.END, f"👤 User: {query}\n")
            return query.lower()
        except:
            speak("Please repeat")
            return "none"


def chatWithGPT(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")  
    log_text.insert(tk.END, "🤖 AI: Thinking...\n")
    app.update_idletasks()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_response = response["choices"][0]["message"]["content"]
   
    log_text.insert(tk.END, "🤖 AI: ")
    app.update_idletasks()
    for char in ai_response:
        log_text.insert(tk.END, char)
        app.update_idletasks()
        time.sleep(0.02)
    log_text.insert(tk.END, "\n\n")

    speak(ai_response)
    return ai_response


def executeCommand(query):
    if 'open youtube' in query:
        webbrowser.open("youtube.com")
        speak("Opening YouTube")
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"Sir, the time is {strTime}")
    elif 'weather' in query:
        search = "temperature in your city"
        url = f"https://www.google.com/search?q={search}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        temp = data.find("div", class_="BNeawe").text
        speak(f"Current temperature is {temp}")
    elif 'ask ai' in query:
        query = query.replace("ask ai", "").strip()
        response = chatWithGPT(query)
        speak(response)
    elif 'exit' in query or 'quit' in query:
        speak("Goodbye!")
        app.quit()
    else:
        speak("I didn't recognize the command.")


def startListening():
    query = takeCommand()
    if query != "none":
        executeCommand(query)


def toggleDarkMode():
    if app.cget("bg") == "#FFFFFF":
        bg_color = "#2E2E2E"
        fg_color = "#FFFFFF"
    else:
        bg_color = "#FFFFFF"
        fg_color = "#000000"

    app.configure(bg=bg_color)
    title.configure(bg=bg_color, fg=fg_color)
    log_text.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    for button in buttons:
        button.configure(bg=bg_color, fg=fg_color)


def changeVoice():
    voices = engine.getProperty('voices')
    current_voice = engine.getProperty('voice')
    new_voice = voices[1].id if current_voice == voices[0].id else voices[0].id
    engine.setProperty('voice', new_voice)
    speak("Voice changed successfully.")


def askAI():
    user_query = entry_box.get()
    if user_query.strip():
        chatWithGPT(user_query)
    else:
        log_text.insert(tk.END, "⚠ Please enter a question.\n")


def guiApp():
    global app, log_text, title, entry_box, buttons

    
    app = tk.Tk()
    app.title("NOVA AI Assistant")
    app.geometry("700x700")
    app.configure(bg="#F0F0F0")

  

    title = tk.Label(app, text="🤖 NOVA AI Assistant", font=("Helvetica", 18, "bold"), bg="#F0F0F0")
    title.pack(pady=5)

   
    log_text = scrolledtext.ScrolledText(app, height=12, width=50, font=("Helvetica", 12))
    log_text.pack(pady=10)

    
    entry_box = tk.Entry(app, width=40, font=("Helvetica", 12))
    entry_box.pack(pady=5)

   
    buttons = [
        tk.Button(app, text="🎤 Speak", font=("Helvetica", 14), command=startListening),
        tk.Button(app, text="Ask AI", font=("Helvetica", 14), command=askAI),
        tk.Button(app, text="About", font=("Helvetica", 14), command=lambda: messagebox.showinfo("About", "NOVA AI Assistant\nDeveloped by Sarthak & Meet")),
        tk.Button(app, text="Toggle Dark Mode", font=("Helvetica", 14), command=toggleDarkMode),
        tk.Button(app, text="Change Voice", font=("Helvetica", 14), command=changeVoice),
        tk.Button(app, text="Quit", font=("Helvetica", 14), command=app.quit),
    ]

    
    for btn in buttons:
        btn.pack(pady=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#555555", fg="white"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="SystemButtonFace", fg="black"))

    app.mainloop()


guiApp()
