# Conversational AI Chatbot with Speech Recognition

This project implements a conversational AI chatbot that uses the [Whisper](https://platform.openai.com/docs/guides/speech-to-text) model to transcribe user speech to text. It utilizes the OpenAI GPT-3.5-turbo/GPT-4 LLM for generating human-like responses. It then synthesizes the output into human-like audio speech output using [Text-to-speech](https://platform.openai.com/docs/guides/text-to-speech).

## Features

- Speech recognition: The chatbot listens to user speech input and converts it into text.
- Interactive responses: The chatbot uses the [Langchain](https://www.langchain.com/), GPT-3.5-turbo/GPT-4 model to generate context-aware and engaging responses.
- Voice output: The chatbot's responses are synthesized into speech using OpenAI [Text-to-speech](https://platform.openai.com/docs/guides/text-to-speech)
- Interactive conversation: The chatbot maintains a memory of past conversations to create a context-rich interaction.

## Usage

1. **Clone the repository to your local machine:**

    ```bash
    git clone 
    ```

2. **Navigate to the project directory:**

    ```bash
    cd speech_recognition_model
    ```

3. **Install project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your OpenAI API key:**

    In the project directory, create a `.env` file and add the following line:
    
    ```
    YOUR_OPENAI_API_KEY='your-openai-api-key'
    ```
    
    Replace `'your-openai-api-key'` with your actual OpenAI API key in the `.env` file.

5. **Run the chatbot:**

    ```bash
    python speech_recognition.py
    ```

    The chatbot will initiate a conversation by greeting you in a friendly manner. You can respond to the chatbot's prompts using your voice. To exit the conversation, say "bye".

## Notes

- Make sure you have an active internet connection to use the OpenAI API.
- You might need to adjust the microphone source in the `listen()` function if you have multiple audio devices.

## Acknowledgments

- This project uses the OpenAI GPT-3.5-turbo/GPT-4 model for generating responses.

## Prerequisites

Ensure you have Python 3.11 or later installed. Install the required packages:

```bash
pip install SpeechRecognition pocketsphinx nltk transformers pyttsx3 schedule googletrans==4.0.0-rc1

## !!!!!! Don't forgot to install the ```PyAudio-0.2.14-cp311-cp311-win32.whl``` On Windows Prompt. It's very Important !!!!!