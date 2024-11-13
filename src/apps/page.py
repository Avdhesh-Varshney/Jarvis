from src.helpers.getFolders import getFolders
from src.helpers.getModules import getModules
from importlib import import_module
import streamlit as st

pathData = {
	"Jarvis": "src/apps/public",
	"Account": "src/auth",
	"Automations": "src/apps/automations",
	"Models": "src/apps/models",
	"Programs": "src/apps/programs",
	"Admin Tools": "src/apps/adminTools"
}

def setRoutes(mainPath):
	modules = getModules(mainPath)
	if modules != {}:
		if st.session_state['verified'] == 'true':
			if 'Login' in modules:
				modules.pop('Login')
				modules.pop('Signup')
		else:
			if 'Profile' in modules:
				modules.pop('Profile')

		chooseProgram = st.sidebar.selectbox("Program", list(modules))
		if chooseProgram in modules:
			try:
				program = modules[chooseProgram]
				module = import_module(f"{mainPath.replace('/', '.')}.{program}")
				func = getattr(module, program)
				func()
			except ModuleNotFoundError:
				st.error(f"Module '{module}.py' could not be found.")
			except AttributeError:
				st.error(f"Function '{program}' could not be found in '{module}.py'.")
			except Exception as e:
				st.error(f"An error occurred: {e}")
		else:
			st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')
	else:
		folders = getFolders(mainPath)
		chooseFolder = st.sidebar.selectbox(f"{mainPath.split('/')[-1].capitalize()}", list(folders))
		if chooseFolder in folders:
			setRoutes(f"{mainPath}/{folders[chooseFolder]}")
		else:
			st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

def application():
	if st.session_state['verified'] == 'true':
		categories = getFolders("src/apps")
		categories.pop("Public")
		if st.session_state.user.split(',')[4] != 'Admin':
			categories.pop("Admin Tools")
		chosenPage = st.sidebar.selectbox("Category", ["Jarvis", "Account"] + list(categories.keys()), key="page")
	else:
		chosenPage = st.sidebar.selectbox("Category", ["Jarvis", "Account"], key="page")
	setRoutes(pathData[chosenPage])
