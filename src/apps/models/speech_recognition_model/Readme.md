# Jarvis - An Offline, Multilingual Virtual Assistant

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

Ensure you have Python 3.7 or later installed. Install the required packages:

```bash
pip install SpeechRecognition pocketsphinx nltk transformers pyttsx3 schedule googletrans==4.0.0-rc1

## !!!!!! Don't forgot to install the ```PyAudio-0.2.14-cp311-cp311-win32.whl``` On Windows Prompt. It's very Important !!!!!