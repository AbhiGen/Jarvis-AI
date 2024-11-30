import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import time
import subprocess

# Initialize the TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index for a different voice

# Global variable to track sleep mode
sleep_mode = False

# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Function to take voice input and convert it to text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        r.pause_threshold = 1  # Adjust to the appropriate pause time for users
        
        try:
            audio = r.listen(source, timeout=15, phrase_time_limit=8)  # Increased timeout and phrase limit
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please speak again.")
            return "None"
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        speak("I didn't understand that. Could you repeat, please?")
        return "None"
    except sr.RequestError:
        speak("There seems to be a problem with the speech service.")
        return "None"
    
    return query

# Function to greet the user based on the time of the day
def wish():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning sir")
    elif 12 <= hour < 18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")
    speak("I am your Jarvis. How can I assist you today?")

# Function to check if Jarvis should wake up
def wake_jarvis():
    global sleep_mode
    while sleep_mode:
        query = takecommand().lower()
        if "jarvis" in query:
            sleep_mode = False
            speak("Yes sir, on your command. How could I assist you?")
            break

# Function to handle the camera and capture photos
def open_camera():
    cap = cv2.VideoCapture(0)
    speak("Camera opened. Say 'capture' to take a photo or 'exit camera' to close the camera.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Failed to capture image.")
            break
        
        cv2.imshow('Webcam', frame)

        # Listening for user commands while camera is open
        query = takecommand().lower()

        if "capture" in query:
            filename = f"photo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(filename, frame)
            speak(f"Photo captured and saved as {filename}")
        elif "exit camera" in query:
            speak("Exiting the camera.")
            break
        
        # Press 'q' to manually quit in case of need
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to send a WhatsApp message
# Example contact dictionary with contact name mapped to phone numbers
contacts = {
    "amma":"+917702282239",
    "pavan":"+916301992996",
    "tharun": "+918074243996",
    "dad": "+919490178435"
}

# Function to send a WhatsApp message with logic to resolve contact names or accept phone numbers
def send_whatsapp_message():
    speak("To whom do you want to send a message?")
    contact_or_number = takecommand().lower()

    # If the user speaks a name, resolve the number
    if contact_or_number in contacts:
        number = contacts[contact_or_number]
        speak(f"Sending message to {contact_or_number}.")
    elif contact_or_number.startswith('+') and len(contact_or_number) >= 10:
        # If the user provides a valid phone number (assume it starts with a '+' and has enough digits)
        number = contact_or_number
        speak(f"Sending message to {number}.")
    else:
        speak(f"I couldn't find {contact_or_number} in your contacts, and it's not a valid number.")
        return

    speak("What message would you like to send?")
    message = takecommand().lower()
    
    # Schedule the message to send in the next minute
    hour = datetime.datetime.now().hour
    minute = (datetime.datetime.now().minute + 1) % 60
    
    kit.sendwhatmsg(number, message, hour, minute)
    speak("Message has been scheduled on WhatsApp.")

# Function to open the weather forecast URL
def check_weather():
    weather_url = "https://www.msn.com/en-in/weather/forecast/in-Coimbatore-South,Tamil-Nadu?loc=eyJsIjoiQ29pbWJhdG9yZSBTb3V0aCIsInIiOiJUYW1pbCBOYWR1IiwiYyI6IkluZGlhIiwiaSI6IklOIiwiZyI6ImVuLWluIiwieCI6Ijc2Ljg5NTgyODI0NzA3MDMxIiwieSI6IjEwLjkwMjM2NjYzODE4MzU5NCJ9&weadegreetype=C&ocid=winp2fptaskbar&cvid=95f263cc15674eedd9a6be12e182be35&fcsttab=detail&day=2"
    webbrowser.open(weather_url)
    speak("Opened the weather forecast for Coimbatore.")

# Function to set an alarm
def set_alarm():
    speak("What time should I set the alarm for? Please mention the time in 24-hour format.")
    alarm_time = takecommand().lower()
    
    try:
        # Parse the time
        alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
        current_time = datetime.datetime.now()
        alarm_time = current_time.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)
        
        # If the alarm time is in the past, set it for the next day
        if alarm_time < current_time:
            alarm_time += datetime.timedelta(days=1)
        
        # Ask for the note before entering the wait loop
        speak("Alarm set. What note would you like to add?")
        note = takecommand()
        
        # Wait until the alarm time is reached
        while datetime.datetime.now() < alarm_time:
            time.sleep(1)
        
        # Ring the alarm and mention the note
        speak(f"Alarm ringing! Note: {note}")
    
    except ValueError:
        speak("I couldn't understand the time format. Please use HH:MM format.")


def play_music_web():
    speak("Which song would you like to play?")
    song = takecommand().lower()
    # Open the web-based music player, e.g., Spotify Web Player or YouTube Music
    webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
    
    # Simple control commands
    while True:
        query = takecommand().lower()
        if "pause" in query:
            speak("Pausing the music.")
            # Simulate pressing the pause button
            subprocess.call(["xdotool", "key", "space"])  # Works on Linux, for Windows you might use `SendKeys`
        elif "play" in query:
            speak("Playing the music.")
            # Simulate pressing the play button
            subprocess.call(["xdotool", "key", "space"])  # Works on Linux, for Windows you might use `SendKeys`
        elif "next" in query:
            speak("Skipping to the next song.")
            # Simulate pressing the next button
            subprocess.call(["xdotool", "key", "Right"])  # Works on Linux, for Windows you might use `SendKeys`
        elif "previous" in query:
            speak("Going back to the previous song.")
            # Simulate pressing the previous button
            subprocess.call(["xdotool", "key", "Left"])  # Works on Linux, for Windows you might use `SendKeys`
        elif "stop" in query or "exit" in query:
            speak("Stopping the music player.")
            break


# Main execution flow
if __name__ == "__main__":
    wish()
    while True:
        if not sleep_mode:
            query = takecommand().lower()

            # Handling tasks based on the recognized command
            if "open notepad" in query:
                os.startfile("notepad.exe")
                sleep_mode = True
                speak("Notepad opened. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            elif "open command prompt" in query:
                os.system("start cmd")
                sleep_mode = True
                speak("Command Prompt opened. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            elif "open vs code" in query:
                os.startfile(r"C:\Users\abhir\AppData\Local\Programs\Microsoft VS Code\Code.exe")
                sleep_mode = True
                speak("VS Code opened. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            elif "open google" in query:
                os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe --profile-directory=\"Profile 1\"")
                sleep_mode = True
                speak("Google Chrome opened. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            elif "open camera" in query:
                open_camera()
                sleep_mode = True
                speak("Camera opened. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            elif "send whatsapp message" in query:
                send_whatsapp_message()
                sleep_mode = True
                speak("WhatsApp message sent. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            elif "open instagram" in query:
                webbrowser.open("https://www.instagram.com")
                sleep_mode = True
                speak("Instagram opened. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address is {ip}")
                sleep_mode = True
                speak("I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            elif "wikipedia" in query:
                speak("Searching Wikipedia")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                print(results)
                sleep_mode = True
                speak("I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            elif "open youtube" in query:
                webbrowser.open("https://www.youtube.com")
                sleep_mode = True
                speak("YouTube opened. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            elif "exit" in query or "goodbye" in query:
                speak("Goodbye! Have a great day!")
                break

            elif "switch voice" in query:
                current_voice = engine.getProperty('voice')
                engine.setProperty('voice', voices[1].id if current_voice == voices[0].id else voices[0].id)
                speak("Voice switched.")

            elif "check weather" in query:
                check_weather()
                sleep_mode = True
                speak("Weather checked. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()

            #elif "play spotify music" in query:
            #    play_spotify_music()
            #    sleep_mode = True
            #   speak("Music playing. I am going to sleep. Say 'Jarvis' to wake me up.")
            #   wake_jarvis()

            elif "set alarm" in query:
                set_alarm()
                sleep_mode = True
                speak("Alarm set. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()
            
            elif "play music" in query:
                play_music_web()
                sleep_mode = True
                speak("Alarm set. I am going to sleep. Say 'Jarvis' to wake me up.")
                wake_jarvis()
