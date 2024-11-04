import speech_recognition as sr
import nltk
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import pyttsx3
import schedule
import json
import time
from datetime import datetime, timedelta
from googletrans import Translator

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

class PowerfulJarvis:
    def __init__(self, wake_words=[("jarvis", 1.0), ("assistant", 0.8)], user_id="default_user"):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_words = wake_words
        self.voice_engine = pyttsx3.init()
        self.user_id = user_id
        self.supported_commands = [
            "check the weather", "tell me the time", "set an alarm",
            "play music", "tell a joke", "fetch news", "remind me"
        ]
        self.translator = Translator()
        self.user_profile = self.load_user_profile()
        self.nlp_pipeline = pipeline(
            "zero-shot-classification",
            model="joeddav/xlm-roberta-large-xnli"
        )
        self.is_active = False
        self.context_mode = False
        self.command_history = []
    
    def load_user_profile(self):
        """Loads user profile from a JSON file or creates a default profile if not found."""
        try:
            with open(f"{self.user_id}_profile.json", "r") as file:
                profile = json.load(file)
                print(f"Loaded profile for {profile['name']}")
                return profile
        except FileNotFoundError:
            print("No profile found, creating a default profile.")
            return {"name": "User", "language": "en", "timezone": "UTC"}

    def save_user_profile(self):
        """Saves user profile to a JSON file."""
        with open(f"{self.user_id}_profile.json", "w") as file:
            json.dump(self.user_profile, file)
    
    def speak(self, text):
        """Uses pyttsx3 for offline voice responses."""
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()

    def listen_for_wake_word(self):
        """Continuously listens for wake words to activate Jarvis."""
        print("Listening for wake words...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                audio = self.recognizer.listen(source)
                try:
                    detected_text = self.recognizer.recognize_sphinx(audio, keyword_entries=self.wake_words)
                    print(f"Detected Wake Word: {detected_text}")
                    if any(wake_word[0] in detected_text.lower() for wake_word in self.wake_words):
                        self.is_active = True
                        self.speak(f"Hello, {self.user_profile['name']}! How can I assist you?")
                        self.listen_for_command()
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print(f"Error in wake word detection: {e}")

    def listen_for_command(self):
        """Listens for a command after activation."""
        print("Listening for command...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command_text = self.recognizer.recognize_sphinx(audio)
                command_text_translated = self.translator.translate(command_text, dest=self.user_profile["language"]).text
                print("Command detected: " + command_text)
                self.process_command(command_text_translated)
            except sr.UnknownValueError:
                self.speak("I couldn't understand. Could you please repeat?")
            except sr.WaitTimeoutError:
                print("Listening timed out.")
            finally:
                if not self.context_mode:
                    self.is_active = False

    def process_command(self, command_text):
        """Processes the recognized command with multilingual NLP support."""
        print(f"Processing command: {command_text}")
        
        classification = self.nlp_pipeline(command_text, self.supported_commands, multi_label=True)
        top_command = classification['labels'][0]
        confidence = classification['scores'][0]
        print(f"Classified Command: {top_command} with confidence {confidence:.2f}")
        
        if confidence > 0.5:
            self.execute_command(top_command)
        else:
            self.speak("I'm not sure how to handle that command. Could you rephrase?")
            self.command_history.append(command_text)

        # Save user profile and recent commands to learn user preferences
        self.save_user_profile()
        
        # Enable continuous mode if requested
        if "continue" in command_text.lower():
            self.context_mode = True
            self.speak("Continuous mode activated.")
        elif "stop" in command_text.lower():
            self.context_mode = False
            self.speak("Continuous mode deactivated.")

    def execute_command(self, command):
        """Executes commands based on classification result."""
        if "weather" in command:
            self.get_weather()
        elif "time" in command:
            self.tell_time()
        elif "alarm" in command:
            self.set_alarm()
        elif "music" in command:
            self.play_music()
        elif "joke" in command:
            self.tell_joke()
        elif "news" in command:
            self.fetch_news()
        elif "remind" in command:
            self.set_reminder()

    # Example command handlers
    def get_weather(self):
        self.speak("Fetching the weather for you...")
    
    def tell_time(self):
        current_time = datetime.now().strftime('%I:%M %p')
        self.speak(f"The current time is {current_time}")

    def set_alarm(self):
        alarm_time = datetime.now() + timedelta(minutes=1)  # Example placeholder
        schedule.every().day.at(alarm_time.strftime("%H:%M")).do(lambda: self.speak("Alarm ringing!"))
        self.speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}")

    def play_music(self):
        self.speak("Playing music...")

    def tell_joke(self):
        self.speak("Here's a joke: Why did the computer get cold? Because it left its Windows open!")

    def fetch_news(self):
        self.speak("Fetching the latest news...")

    def set_reminder(self):
        reminder_time = datetime.now() + timedelta(minutes=2)  # Example placeholder
        schedule.every().day.at(reminder_time.strftime("%H:%M")).do(lambda: self.speak("This is your reminder!"))
        self.speak("Reminder has been set.")

    def start(self):
        """Starts the continuous wake word detection loop and scheduled tasks checker."""
        try:
            self.listen_for_wake_word()
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nJarvis has been stopped.")

# Example usage
if __name__ == "__main__":
    jarvis = PowerfulJarvis()
    jarvis.start()
