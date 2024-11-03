import os
import openai
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
from config import apikey

openai.api_key = apikey

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id) 

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's voice command and convert it to text"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
    return None

def search_web(query, engine="google"):
    """Search the web for a query using the specified search engine."""
    search_engines = {
        "google": "https://www.google.com/search?q={}",
        "brave": "https://search.brave.com/search?q={}"
    }

    if engine in search_engines:
        search_url = search_engines[engine].format(query)
    else:
        speak(f"Search engine {engine} not found. Defaulting to Google.")
        search_url = search_engines["google"].format(query)

    speak(f"Searching for {query} on {engine}.")

    try:
        webbrowser.open(search_url)
    except Exception as e:
        speak("Sorry, I couldn't open the browser.")
        print(f"Error: {e}")


def perform_task(command):
    """Perform tasks based on recognized command"""
    if 'play' in command:
        song = command.replace('play', '').strip()
        speak(f'Playing {song}')
        pywhatkit.playonyt(song)
    elif 'time' in command:
        speak(f'Current time is {datetime.datetime.now().strftime("%I:%M %p")}')
    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        speak(wikipedia.summary(person, sentences=1))
    elif 'open youtube' in command:
        webbrowser.open('https://www.youtube.com')
    elif 'open google' in command:
        webbrowser.open('https://www.google.com')
    elif 'open stack overflow' in command:
        webbrowser.open('https://stackoverflow.com')
    elif 'shut down' in command:
        speak('Shutting down the system.')
        os.system('shutdown /s /t 1')
    elif 'search' in command:
        query = command.replace('search', '').strip()
        search_web(query)
    elif 'who made you' in command:
        speak('The Raghav Sharma is my creator.')
    else:
        speak('Sorry, I cannot perform that task.')

def main():
    speak("Hello, I am Ashy. How can I help you today?")
    while True:
        command = listen()
        if command:
            if 'Bye' in command:
                speak('Bye Raghav')
                break
            perform_task(command)

if __name__ == '__main__':
    main()
