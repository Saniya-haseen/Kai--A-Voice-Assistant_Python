import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import time
import datetime
import psutil
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("User said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that. Please say again.")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return ""

def get_date():
    today = datetime.date.today().strftime("%B %d, %Y")
    return f"Today's date is {today}."

def get_battery():
    battery = psutil.sensors_battery()
    if battery:
        return f"The battery is at {battery.percent} percent."
    else:
        return "Battery information is not available."

def set_volume(change):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current = volume.GetMasterVolumeLevelScalar()
    new_volume = min(max(current + change, 0.0), 1.0)
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    speak(f"Volume set to {int(new_volume * 100)} percent.")

def adjust_brightness(change):
    try:
        current = sbc.get_brightness()[0]
        new_level = min(max(current + change, 0), 100)
        sbc.set_brightness(new_level)
        speak(f"Brightness set to {new_level} percent.")
    except:
        speak("I couldn't change the brightness.")

def execute_command(command):
    if 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'open chat gpt' in command:
        speak("Opening ChatGPT")
        webbrowser.open("https://chat.openai.com")
    elif 'open linkedin' in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    elif 'open whatsapp' in command:
        speak("Opening WhatsApp Web")
        webbrowser.open("https://web.whatsapp.com")
    elif 'open gmail' in command:
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com")
    elif 'open github' in command:
        speak("Opening GitHub")
        webbrowser.open("https://github.com/")
    elif 'what is the time' in command or 'tell me the time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif 'what is the date' in command or 'tell me the date' in command:
        speak(get_date())
    elif 'battery' in command:
        speak(get_battery())
    elif 'increase volume' in command:
        set_volume(0.1)
    elif 'decrease volume' in command:
        set_volume(-0.1)
    elif 'increase brightness' in command:
        adjust_brightness(10)
    elif 'decrease brightness' in command:
        adjust_brightness(-10)
    elif 'exit' in command or 'stop' in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I can't perform that action yet.")

if __name__ == "__main__":
    speak("Kai here boss. How can I help you?")
    while True:
        command = take_command()
        if command.strip():
            execute_command(command)
