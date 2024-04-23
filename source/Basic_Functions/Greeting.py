from datetime import datetime

def GreetUser():
    hour = datetime.now().hour
    if(hour >= 6) and (hour < 11):
        return "Good Morning Sir!!"
    elif(hour >= 11) and (hour < 17):
        return "Good Afternoon Sir!!"
    elif(hour >= 17) and (hour < 19):
        return "Good Evening Sir!!"
    return "Good Night Sir!!"
