import streamlit as st
import smtplib

def EMail():
	st.markdown("#### Welcome to E-mail Automation")
	senderEmail = st.text_input("Enter your E-mail Address")
	passWord = st.text_input("Enter your Password", type="password")

	receiverEmail = st.text_input("Enter the Recipient's E-mail Address")
	content = st.text_area("Enter the content for the mail")

	if st.button("Send Mail"):
		if senderEmail != "" and passWord != "" and receiverEmail != "" and content != "":
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.login(senderEmail, passWord)
			server.sendmail(senderEmail, receiverEmail, content)
			server.close()
			st.success("E-mail has sent.", icon="✅")
		else:
			st.error("Please provide all the details.", icon="🚨")
	st.info(f'''Switch on the 'Less secure app access' of sender's mail by using this [link](https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4MWL7anq0zxK7rt3arv3YBLKrAswWmAWqOkIUCd0qKKHlpQyezvEt2ruMNK2BaXddqMJlydydf-quRjLpwabeoLI_tZ3Q).''', icon="ℹ️")
