from streamlit_ws_localstorage import injectWebsocketCode
import uuid

def server():
	return injectWebsocketCode(hostPort='wsauthserver.supergroup.ai', uid=str(uuid.uuid1()))
