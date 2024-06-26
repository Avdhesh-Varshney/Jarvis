import sys
from playsound import playsound
import pyjokes
from pywikihow import search_wikihow
from win10toast import ToastNotifier
import streamlit as st
sys.path.insert(1, './Code/')
from BasicFunctions.English import Speak, Listen
from BasicFunctions.Hindi import SpeakH, ListenH
from BasicFunctions.ParseCommand import Parse
from Features.ChatBot.ChatBot import ChatterBot

from Features.CasualPro.Advice import Advice
from Features.CasualPro.FindIP import FindMyIp
from Features.CasualPro.Jokes import Joke
from Features.CasualPro.MyLocation import My_Location

from Features.ApiPro.AIBrain import ReplyBrain
from Features.ApiPro.Calculator import Calculator
from Features.ApiPro.Temperature import Temperature
from Features.ApiPro.Movies import TrendingMovies
from Features.ApiPro.Weather import WeatherReport
from Features.ApiPro.News import latestNews
from Features.ApiPro.Nasa import NasaNews, MarsImage, Astro, SolarBodies
from Features.ApiPro.TV import SearchMovieTitle, MovieRecommendations, PopularMovies, MovieInfo, SimilarMovies, TheatresMovies, DiscoverPopularMovies, DiscoverKidsMovies, SearchTVShowsTitle, SimilarTVShows, ShowsSeason, PersonDetails

from Features.BasicPro.Alarm import Alarm
from Features.BasicPro.Remember import RememberMSG, Remind
from Features.BasicPro.ScreenShot import screenshot
from Features.BasicPro.SpeedTest import SpeedTest

from Features.DataPro.CoronaVirus import CoronaVirus
from Features.DataPro.Website import website

from Features.StudyPro.Dictionary import Dict
from Features.StudyPro.OnlineClasses import OnlineClass
from Features.StudyPro.ReadTextBook import Reader
from Features.StudyPro.TimeTable import TimeTable
from Features.StudyPro.Wikipedia import wiki
from Features.StudyPro.Translator import TranEnHi, TranHiEn

from Features.Games.Games import Game

from Automations.Messengers.Email import sendEmail
from Automations.Messengers.Telegram import Telegram
from Automations.Messengers.Whatsapp import Whatsapp

from Automations.TextEditors.Notepad import Notepad
from Automations.TextEditors.Wordpad import Wordpad

from Automations.WindowApps.CloseApps import CloseApps
from Automations.WindowApps.OpenApps import OpenApps

from Automations.Websites.Google import Google
from Automations.Websites.GoogleMaps import GoogleMaps
from Automations.Websites.YouTube import YouTube

def CasualExe(command):
    if 'advice' in command:
        return Advice()
    elif 'ip address' in command:
        return FindMyIp()
    elif 'joke' in command:
        return Joke()
    elif 'my location' in command:
        return My_Location()
    return None

def ApiExe(command):
    if 'calculator' in command:
        api_key = st.text_input('Enter WolfRam Api Key:')
        query = st.text_input('Enter the calculation:')
        st.info('Get Api key from here, https://www.wolframalpha.com/', icon="ℹ️")
        return Calculator(query, api_key)
    elif 'temperature' in command:
        api_key = st.text_input('Enter WolfRam Api Key:')
        query = st.text_input('Name of Place:')
        st.info('Get Api key from here, https://www.wolframalpha.com/', icon="ℹ️")
        return Temperature(query, api_key)
    elif 'weather' in command:
        OPENWEATHER_APP_ID = st.text_input('Enter Open Weather App ID:')
        place = st.text_input('Name of Place:')
        WeatherReport(place, OPENWEATHER_APP_ID)
        return 1
    elif 'news' in command:
        NEWS_API_KEY = st.text_input('Enter News Api Key:')
        latestNews(NEWS_API_KEY)
        return 1
    elif 'space news' in command:
        Api_Key = st.text_input('Enter Nasa Api Key:')
        NasaNews(Api_Key)
        return 1
    elif 'mars images' in command:
        MarsImage()
        return 1
    elif 'asteroids' in command:
        Astro()
        return 1
    elif 'solar system' in command:
        SolarBodies()
        return 1
    elif 'movies' in command:
        return Movies(command)
    elif 'tv' in command or 'actor' in command:
        return tvShows(command)
    return None

def Movies(command):
    if 'popular movies' in command:
        Speak("Do you know the id of the movie that are related you want ? (yes/no)")
        flag = Listen()
        if flag == 'yes':
            DiscoverPopularMovies()
        else:
            PopularMovies()
        return 1
    elif 'trending movies' in command or 'latest movies' in command:
        TrendingMovies()
        return 1
    elif 'movie recommendation' in command:
        MovieRecommendations()
        return 1
    elif 'similar movies' in command:
        SimilarMovies()
        return 1
    elif 'movies details' in command:
        Speak("Do you know the id of the movie ? (yes/no)")
        flag = Listen()
        if flag == 'yes':
            MovieInfo()
        else:
            SearchMovieTitle(command)
        return 1
    elif 'kids movies' in command:
        DiscoverKidsMovies()
        return 1
    elif 'theatre movies' in command:
        TheatresMovies()
        return 1
    return None

def tvShows(command):
    if 'tv shows' in command:
        Speak("Do you know the id of the drama or show? (yes/no)")
        flag = Listen()
        if flag == 'yes':
            SimilarTVShows()
        else:
            SearchTVShowsTitle()
        return 1
    elif 'episodes' in command or 'seasons' in command:
        ShowsSeason()
        return 1
    elif 'actor details' in command:
        PersonDetails()
        return 1
    return None

def BasicExe(command):
    if 'alarm' in command:
        query = Parse(command)
        Alarm(query)
        return 1
    elif 'remember that' in command:
        query = Parse(command)
        RememberMSG(query)
        return 1
    elif 'what do you remember' in command:
        Remind()
        return 1
    elif 'screenshot' in command:
        screenshot()
        return 1
    elif 'speed' in command:
        return SpeedTest(command)
    return None

def DataExe(command):
    if 'cases of corona' in command:
        CoronaVirus()
        return 1
    elif 'website' in command:
        query = Parse(command)
        website(query)
        return 1
    return None

def StudyExe(command):
    if 'meaning' in command or 'synonym' in command or 'similar' in command or 'antonym' in command or 'opposite' in command:
        query = Parse(command)
        return Dict(query)
    elif 'online class' in command:
        Speak("Tell Me The Name Of the Class.")
        Subject = Listen()
        OnlineClass(Subject)
        return 1
    elif 'read book' in command:
        Reader()
        return 1
    elif 'time table' in command:
        TimeTable()
        return 1
    elif 'wikipedia' in command:
        wiki()
        return 1
    elif 'english to hindi' in command or 'convert it into hindi' in command:
        command = command.replace("english to hindi", "")
        command = command.replace('convert it into hindi', '')
        SpeakH(TranEnHi(command))
        return 1
    elif 'hindi to english' in command or 'convert it into english' in command:
        command = command.replace("hindi to english", "")
        command = command.replace('convert it into english', '')
        return TranHiEn(command)
    return None

def DirectExe(command):
    if 'introduce' in command:
        playsound('./Main/DataBase/Audios/Jarvis.mp3')
    elif 'jokes' in command:
        return pyjokes.get_joke()
    elif 'repeat my words' in command:
        Speak("Yes Sir!")
        query = Listen()
        return f"You Said : {query}"
    elif 'how to' in command:
        Speak("Getting data from the internet...")
        op = command.replace("jarvis", "")
        how_to_func = search_wikihow(op, 1)
        assert len(how_to_func) == 1
        how_to_func[0].print()
        return how_to_func[0].summary
    return None

def MessengersExe(command):
    if 'whatsapp' in command:
        Whatsapp()
        return 1
    elif 'telegram' in command:
        Telegram()
        return 1
    elif 'email' in command:
        sendEmail()
        return 1
    return None

def TextEditorsExe(command):
    if 'notepad' in command:
        Notepad()
        return 1
    elif 'wordpad' in command:
        Wordpad()
        return 1
    return None

def WindowAppsExe(command):
    if 'close' in command:
        query = Parse(command)
        CloseApps(query)
        return 1
    elif 'open' in command:
        query = Parse(command)
        OpenApps(query)
        return 1
    return None

def WebsitesExe(command):
    if 'google' in command:
        Speak("Searching on Google...")
        query = Parse(command)
        Google(query)
        return 1
    elif 'google maps' in command:
        Speak("Getting directions from Google Maps...")
        query = Parse(command)
        GoogleMaps()
        return 1
    elif 'youtube' in command:
        Speak("Searching on YouTube...")
        query = Parse(command)
        YouTube(query)
        return 1
    return None

def CommandCheck(command):
    if 'game' in command or 'games' in command:
        Game()
        return
    result = CasualExe(command)
    if result is None:
        result = ApiExe(command)
    if result is None:
        result = BasicExe(command)
    if result is None:
        result = DataExe(command)
    if result is None:
        result = StudyExe(command)
    if result is None:
        result = DirectExe(command)
    if result is None:
        result = MessengersExe(command)
    if result is None:
        result = TextEditorsExe(command)
    if result is None:
        result = WindowAppsExe(command)
    if result is None:
        result = WebsitesExe(command)
    if result is not None and result != 1:
        Speak(result)
    if result is None and result != 1:
        try:
            Speak(ChatterBot(command))
        except:
            Speak(ReplyBrain(command))

def TaskExe(choice):
    toast = ToastNotifier()
    toast.show_toast("Jarvis", "The Jarvis is now activated...", duration = 3)
    choice = choice.lower()
    CommandCheck(choice)

# TaskExe()
