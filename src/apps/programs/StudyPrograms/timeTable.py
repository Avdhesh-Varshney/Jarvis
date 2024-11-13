import streamlit as st

def timeTable():
  from notifypy import Notify
  st.write("Checking...")

  from DataBase.TimeTable.Sunday import Time

  value = Time()

  Noti = Notify()
  Noti.title = "TimeTable"
  Noti.message = str(value)
  # Noti.icon = "Give path of the icon"
  Noti.send()

  st.write("Anything Else Sir !!")
