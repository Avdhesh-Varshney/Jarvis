from datetime import datetime

def GreetUser(name):
	hour = datetime.now().hour
	if(hour >= 6) and (hour < 11):
		return ("Good Morning "+ name)
	elif(hour >= 11) and (hour < 17):
		return ("Good Afternoon "+ name)
	elif(hour >= 17) and (hour < 19):
		return ("Good Evening "+name)
	return ("Good Night "+ name)
