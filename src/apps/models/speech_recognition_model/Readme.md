## Jarvis - An Offline, Multilingual Virtual Assistant

Jarvis is an advanced offline virtual assistant powered by a multilingual NLP model, speech recognition, and text-to-speech capabilities. This assistant can respond to various commands, set alarms, fetch news, provide reminders, and more—all with customizable user profiles and support for multiple languages. Perfect for privacy-sensitive, offline applications, Jarvis learns and adapts based on user interactions.

## Features

- **Offline Speech Recognition**: Utilizes `pocketsphinx` for wake word detection and command recognition.
- **Multilingual Support**: Incorporates `googletrans` and `xlm-roberta-large-xnli` for multi-language command processing.
- **Personalized User Profiles**: User-specific profiles (name, language, timezone) are stored and loaded from JSON files.
- **Continuous Learning**: Remembers misunderstood commands for potential future improvements.
- **Context Mode**: Allows for continuous conversation with context switching.
- **Reminders and Alarms**: Includes scheduling and reminders with real-time notifications.
- **Voice Responses**: Uses `pyttsx3` for offline text-to-speech to provide responses.

## Prerequisites

Ensure you have Python 3.11 or later installed. Install the required packages:

```bash
pip install SpeechRecognition pocketsphinx nltk transformers pyttsx3 schedule googletrans==4.0.0-rc1
```
## !!!!!! Don't forgot to install the ```PyAudio-0.2.14-cp311-cp311-win32.whl``` On Windows Prompt. It's very Important !!!!!
```bash
pip install PyAudio-0.2.14-cp311-cp311-win32.whl # For 32bit Windows
```
## How to Use
1. **Start the Assistant:** Run the assistant by executing the main script. This will initialize PowerfulJarvis and start listening for wake words.
```bash
python speech_recognition.py
```
2. **Set Up User Profile:**
- When you first run Jarvis, it will create a default user profile.
- The profile file ```(<username>_profile.json)``` is saved locally with your preferences (name, language, timezone).
- Edit this file if you wish to change settings or provide specific preferences.
3. **Supported Commands:** Once you activate Jarvis by saying a wake word like “Jarvis” or “Assistant,” it will listen for commands. Here are some examples:
- “Check the weather”: Jarvis will respond with a placeholder weather update.
- “Tell me the time”: Jarvis will tell you the current time.
- “Set an alarm”: Jarvis will set an alarm for a specified time.
- “Remind me”: Jarvis can set reminders and notify you at a specified time.
- “Fetch news”: Jarvis will give a placeholder response for news.
- “Translate”: Jarvis can translate text into your preferred language (requires internet).

**Made with ❤️ by Dinmay.**
