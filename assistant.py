import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import pyjokes
import os
import pyautogui

# speech engine initialization

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  


# Speak function

def speak(text):
    print("Daisy:", text)
    engine.say(text)
    engine.runAndWait()


# List available microphones and select internal mic automatically

def get_microphone_index():
    mic_list = sr.Microphone.list_microphone_names()
    print("Available Microphones:")
    for i, mic in enumerate(mic_list):
        print(f"{i}: {mic}")
    
    # Try to select internal mic or return default
    for i, mic in enumerate(mic_list):
        if "microphone" in mic.lower() or "internal" in mic.lower():
            return i
    return None  # fallback to default if nothing matches

mic_index = get_microphone_index()



# Listen function with optional device index

def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand what you said.")
    except sr.RequestError:
        speak("Could not request results. Please check your internet.")
    except Exception as e:
        speak("Sorry, an error occurred with the microphone.")
        print(e)
    return ""



# Greet :-

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Daisy. How can I assist you?")



# Google search:-

def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    speak(f"Here's what I found for {query} on Google.")



# Open website :-

def open_website(site):
    site = site.replace(" ", "")         # removing spaces

    common_sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "linkedin": "https://www.linkedin.com",
        "gmail": "https://mail.google.com",
        "reddit": "https://www.reddit.com/?rdt=33494"
    }

    if site in common_sites:
        webbrowser.open(common_sites[site])
        speak(f"Opening {site}")
    else:
        if not site.startswith("http"):
            site = f"https://{site}.com"           # assume it's a .com 
        webbrowser.open(site)
        speak(f"Opening {site}")


# Closing tab

def close_tab():
    try:
        pyautogui.hotkey('ctrl', 'w')
        speak("Closing the current tab.")
    except Exception as e:
        speak("I couldn't close the tab.")
        print(e)


# Take screenshot with timestamp

def take_screenshot():
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = pyautogui.screenshot()
    screenshot.save(f"data/screenshot_{timestamp}.png")
    speak("Screenshot taken and saved in the data folder.")


# Telling joke

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)


# Telling current date and time

def tell_date_and_time():
    now = datetime.datetime.now()
    date = now.strftime("%A, %B %d, %Y")
    time = now.strftime("%I:%M %p")
    speak(f"Today is {date} and the time is {time}")


# Taking note and save

def take_note():
    os.makedirs("data", exist_ok=True)
    speak("What would you like me to note?")
    note = listen()
    if note:
        with open("data/notes.txt", "a") as f:
            f.write(f"{datetime.datetime.now()}:\n{note}\n\n")
        speak("Note saved in the data folder.")
    else:
        speak("Nothing noted.")




# Main program :-

def main():
    greet()
    while True:
        command = listen()

        if not command:
            continue

        if "search" in command:
            query = command.replace("search", "").strip()
            if query:
                google_search(query)
            else:
                speak("What should I search for?")

        elif "open" in command:
            site = command.replace("open", "").strip()
            open_website(site)

        elif "close tab" in command or "close this" in command:
            close_tab()

        elif "screenshot" in command:
            take_screenshot()

        elif "joke" in command:
            tell_joke()

        elif "date" in command or "time" in command:
            tell_date_and_time()

        elif "note" in command or "write this" in command:
            take_note()

        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that. Try again.")

# Run Daisy
if __name__ == "__main__":
    main()
