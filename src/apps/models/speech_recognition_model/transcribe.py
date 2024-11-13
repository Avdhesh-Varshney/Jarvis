from openai import OpenAI
from dotenv import load_dotenv
import os
import speech_recognition as sr
import uuid

# load environment variables
load_dotenv()

class Transcribe:
    def __init__(self):
        # initialize the OpenAI client
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # folder path to save audio to be transcribed
        self.audio_path = 'user_speech/'

    def record_audio(self):
        # Create a Recognizer instance
        recognizer = sr.Recognizer()

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Recording...")

            # Adjust for ambient noise before recording
            recognizer.adjust_for_ambient_noise(source)

            # Record audio
            audio_data = recognizer.listen(source)

            print("Finished recording.")
        file_path = f'{self.audio_path}{uuid.uuid4()}-audio.wav'
        # Save the recorded audio to a WAV file
        with open(file_path, 'wb') as f:
            f.write(audio_data.get_wav_data())
            
        return file_path

    def transcribe_audio(self, audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcript
    
    def delete_wav_audio_files(self):
        try:
            # List all files in the folder
            files = os.listdir(self.audio_path)

            # Filter only .mp3 files
            wav_files = [file for file in files if file.endswith(".wav")]

            # Delete each .mp3 file
            for wav_file in wav_files:
                file_path = os.path.join(self.audio_path, wav_file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except PermissionError as e:
                    print(f"Skipped: {file_path} (File in use)")

            print("Deletion completed.")

        except FileNotFoundError:
            print(f"Folder not found: {self.audio_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":    
    # Record audio
    transcriber = Transcribe()
    file_path = transcriber.record_audio()
    print(f"Audio recorded and saved to {file_path}")

    # Transcribe audio
    transcript_result = transcriber.transcribe_audio(file_path)
    print("Transcription Result:")
    print(transcript_result)
    transcriber.delete_wav_audio_files()