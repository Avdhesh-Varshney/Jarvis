import random
from datetime import datetime

import pytz


def GreetUser(name):
  india_tz = pytz.timezone("Asia/Kolkata")
  hour = datetime.now(india_tz).hour
  if 5 <= hour < 11:
    return f"Good Morning, {name}"
  elif 11 <= hour < 17:
    return f"Good Afternoon, {name}"
  elif 17 <= hour < 21:
    return f"Good Evening, {name}"
  return f"Good Night, {name}"


def GetRandomWelcomeMessage():
  """Returns a random welcome message to make Jarvis feel more dynamic and natural."""
  welcome_messages = [
    "I am Jarvis Sir. Please tell me how may I help you.",
    "Ready to assist you with anything you need!",
    "At your service! What can I do for you today?",
    "Hello! I'm here to make your day easier.",
    "Great to see you! How can I assist you?",
    "I'm all set to help you out. What's on your mind?",
    "Standing by to help with whatever you need!",
    "Your AI assistant is ready. What would you like to do?",
    "Here to help! Just let me know what you need.",
    "Ready and waiting to assist you today!",
  ]
  return random.choice(welcome_messages)
