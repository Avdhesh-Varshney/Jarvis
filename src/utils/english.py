import pyttsx3
import speech_recognition as sr

def Speak(audio):
	engine = pyttsx3.init('sapi5')
	voices = engine.getProperty('voices')
	engine.setProperty('voices',voices[0].id)
	engine.setProperty('rate',160)
	engine.say(audio)
	engine.runAndWait()

def recognize_speech_from_mic(recognizer, microphone):
	if not isinstance(recognizer, sr.Recognizer):
		raise TypeError("`recognizer` must be `Recognizer` instance")
	if not isinstance(microphone, sr.Microphone):
		raise TypeError("`microphone` must be `Microphone` instance")
	with microphone as source:
		recognizer.adjust_for_ambient_noise(source)
		audio = recognizer.listen(source)
	response = {
		"success": True,
		"error": None,
		"transcription": None
	}
	try:
		response["transcription"] = recognizer.recognize_google(audio)
	except sr.RequestError:
		response["success"] = False
		response["error"] = "API unavailable"
	except sr.UnknownValueError:
		response["error"] = "Unable to recognize speech"
	return response

def Listen():
	PROMPT_LIMIT = 2
	recognizer = sr.Recognizer()
	microphone = sr.Microphone()
	for j in range(PROMPT_LIMIT):
		print('Guess {}. Speak!'.format(j+1))
		guess = recognize_speech_from_mic(recognizer, microphone)
		if guess["transcription"]:
			break
		if not guess["success"]:
			break
	print("I didn't catch that")
	if guess["error"]:
		print("ERROR: {}".format(guess["error"]))
	else:
		print("You said: {}".format(guess["transcription"]))
	return guess["transcription"]
