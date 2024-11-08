from openai import OpenAI
import os
from dotenv import load_dotenv
import pygame
import time
import uuid

# load environment variables
load_dotenv()

class Voice:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Choose a different directory for saving the generated speech
        self.speech_file_path = "speech/"
        
        # list of all available voices
        self.voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        
        
    def generate_voice(self, input_text): 
        '''
            Convert text to speech in a natural voice
        '''       
        response = self.client.audio.speech.create(
            model='tts-1',
            voice='onyx',
            input=input_text
        )

        response_id = f'{self.speech_file_path}{uuid.uuid4()}-response.mp3'
        response.stream_to_file(response_id)
        return response_id

    def play_voice(self, response_id):
        try:
            pygame.mixer.music.load(response_id)
            print(f"Playing: {response_id}")
            pygame.mixer.music.play()

            # Wait until the music finishes playing
            while pygame.mixer.music.get_busy():
                time.sleep(1)

        except pygame.error:
            print(f"Error loading or playing the file: {self.speech_file_path}")
            
    def delete_mp3_files(self):
        try:
            # List all files in the folder
            files = os.listdir(self.speech_file_path)

            # Filter only .mp3 files
            mp3_files = [file for file in files if file.endswith(".mp3")]

            # Delete each .mp3 file
            for mp3_file in mp3_files:
                file_path = os.path.join(self.speech_file_path, mp3_file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except PermissionError as e:
                    print(f"Skipped: {file_path} (File in use)")

            print("Deletion completed.")

        except FileNotFoundError:
            print(f"Folder not found: {self.speech_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")