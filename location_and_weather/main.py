import speech_recognition as sr
import pyttsx3
import requests

# Function to get public IP address using ipify
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text  # Return the public IP address
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Function to fetch location details from ipinfo.io
def get_location_from_ip(ip_address):
    url = f'https://ipinfo.io/{ip_address}/json'

    try:
        response = requests.get(url)
        data = response.json()

        # Check if the response is successful
        if response.status_code == 200:
            location_info = {
                "IP": ip_address,
                "City": data.get("city"),
                "Region": data.get("region"),
                "Country": data.get("country"),
                "Location (Latitude, Longitude)": data.get("loc"),
                "Postal Code": data.get("postal"),
                "Timezone": data.get("timezone")
            }
            return location_info
        else:
            return f"Error: Unable to fetch location data. API returned status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Function to get weather information using wttr.in
def get_weather(city_name):
    url = f"http://wttr.in/{city_name}?format=%C+%t+%w"  # Fetch weather in a simple format
    try:
        response = requests.get(url)
        return response.text.strip()  # Return the weather information as text
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Function to speak the assistant's response
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to listen for a voice command
def listen_for_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Listen for command
    with mic as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()  # Convert speech to text
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return None
    except sr.RequestError:
        speak("Sorry, there was an error with the speech service.")
        return None

# Main function to run the assistant
def run_assistant():
    speak("How can I assist you today?")
    while True:
        command = listen_for_command()

        if command:
            if "location" in command or "where am i" in command:
                speak("Fetching your location automatically...")
                public_ip = get_public_ip()
                location = get_location_from_ip(public_ip)

                if isinstance(location, dict):
                    location_info = f"Your IP is {location['IP']}. You are in {location['City']}, {location['Region']}, {location['Country']}. Your coordinates are {location['Location (Latitude, Longitude)']}. The postal code is {location['Postal Code']}."
                    speak(location_info)
                else:
                    speak(location)  # Speak the error message if any

            elif "weather" in command:
                speak("Fetching your weather automatically...")
                public_ip = get_public_ip()
                location = get_location_from_ip(public_ip)
                
                if isinstance(location, dict):
                    city_name = location["City"]
                    if city_name:
                        weather = get_weather(city_name)

                        if weather:
                            weather_info = f"The current weather in {city_name} is {weather}."
                            speak(weather_info)
                        else:
                            speak("Sorry, I couldn't fetch the weather details.")
                    else:
                        speak("Sorry, I couldn't detect your city automatically for the weather.")
            
            elif "exit" in command or "stop" in command:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I can only tell you your location or weather. Please ask me about that or say 'exit' to quit.")

# Run the assistant
if __name__ == "__main__":
    run_assistant()
