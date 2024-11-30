import pyttsx3
import speech_recognition as sr

# Initialize the TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index for a different voice

# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Function to take voice input and convert it to text
def takecommand():
    r = sr.Recognizer()
    
    # Optional: List available microphones and set the correct one
    # You can uncomment this part to see the available microphone devices
    """
    mic_list = sr.Microphone.list_microphone_names()
    for index, microphone_name in enumerate(mic_list):
        print(f"Microphone {index}: {microphone_name}")
    """

    # Choose the correct microphone if needed, or use the default
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)  # Adjusts for ambient noise
        r.pause_threshold = 1  # Adjust the pause between phrases
        
        try:
            # Listen to input, with reasonable timeout and phrase limits
            audio = r.listen(source, timeout=15, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please speak again.")
            return "None"
        except sr.RequestError as e:
            speak("There was an issue with the microphone.")
            print(f"Error: {str(e)}")
            return "None"
        
    try:
        print("Recognizing...")
        # Recognize speech using Google Speech Recognition
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        speak("I didn't understand that. Could you repeat, please?")
        return "None"
    except sr.RequestError as e:
        speak("I am having trouble accessing the speech service. Please check your connection.")
        print(f"Error: {str(e)}")
        return "None"
    
    return query

# Test function
if __name__ == "__main__":
    speak("Testing microphone recognition.")
    query = takecommand()
    if query != "None":
        speak(f"You said: {query}")
