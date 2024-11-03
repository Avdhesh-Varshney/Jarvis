import streamlit as st
import time

def timer():
	st.subheader("Timer")
	st.write("This is a simple timer application.")

	hour = st.number_input("Hour", 0, 23, 0)
	minute = st.number_input("Minute", 0, 59, 0)
	second = st.number_input("Second", 0, 59, 0)

	if st.button("Start Timer"):
		countdown_time = hour * 3600 + minute * 60 + second

		timer_message = st.empty()
		timer_message.info(f'Timer set for {hour} hours, {minute} minutes, and {second} seconds.', icon="🕒")

		while countdown_time:
			min, sec = divmod(countdown_time, 60)
			hour, min = divmod(min, 60)
			timer_message.info(f'Timer set for {hour} hours, {min} minutes, and {sec} seconds.', icon="🕒")
			countdown_time -= 1
			time.sleep(1)

		timer_message.success("Time's up!", icon="🎉")
