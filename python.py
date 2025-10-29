"""
Filename: jarvis_auth.py
Title: Jarvis — Streamlit Auth & Welcome Page
Description:
  Single-file Streamlit page for Jarvis that displays a personalized welcome,
  Google-based authentication buttons, user profile (picture, name, email),
  and handles login/logout flow. Uses IST time helper for timestamp formatting
  and safe UI flows. Place this file in your Streamlit app (e.g., at the app root
  or in the `pages/` folder) and run with `streamlit run jarvis_auth.py`.
"""

from datetime import datetime
from time import sleep

import pytz
import streamlit as st

# Replace these imports with your project's actual utility functions.
# If you don't have src/utils/greeting.py, either create it or inline equivalent functions.
try:
    from src.utils.greeting import GetRandomWelcomeMessage, GreetUser
except Exception:
    # Fallback implementations if src.utils.greeting is not available.
    import random

    def GetRandomWelcomeMessage():
        msgs = [
            "Ready when you are — how can I help?",
            "Good to see you! What would you like to do today?",
            "Nice! I'm standing by for your command.",
            "Welcome back — let's be productive!",
        ]
        return random.choice(msgs)

    def GreetUser(name: str) -> str:
        if not name:
            return "Hello"
        # simple greeting based on hour
        try:
            hour = datetime.now().hour
            if hour < 12:
                prefix = "Good morning"
            elif hour < 18:
                prefix = "Good afternoon"
            else:
                prefix = "Good evening"
            return f"{prefix}, {name}"
        except Exception:
            return f"Hello, {name or 'there'}"


def unix_to_ist(timestamp: float) -> str:
    """
    Convert a UNIX timestamp (seconds) to a human-readable IST time string.

    Args:
      timestamp: seconds since epoch (float or int).

    Returns:
      Formatted string like "07:34:21 PM IST".
    """
    india_tz = pytz.timezone("Asia/Kolkata")
    format_str = "%I:%M:%S %p IST"
    # Ensure timestamp is numeric
    try:
        return datetime.fromtimestamp(float(timestamp), pytz.utc).astimezone(india_tz).strftime(format_str)
    except Exception:
        return "--:--:-- IST"


def auth():
    """
    Streamlit UI for authentication + profile display.

    Note: This relies on Streamlit's built-in `st.login()` / `st.logout()` behavior
    which may be provided by a community auth component or a Streamlit Enterprise feature.
    If your environment doesn't support `st.user`, replace the checks with your app's auth flow.
    """
    # Defensive check: some Streamlit environments won't have st.user
    st.set_page_config(page_title="Jarvis — Welcome", layout="centered")

    # Title block
    st.markdown("## ⚡ Jarvis — Virtual AI Assistant")
    st.write(
        "Jarvis simplifies your daily tasks using natural language automation, "
        "device control and personalized interactions. Sign in to access your profile."
    )
    st.write("---")

    # If the environment has st.user object (Streamlit Cloud / Enterprise), use it.
    use_st_user = hasattr(st, "user")

    if use_st_user:
        try:
            user_obj = st.user
        except Exception:
            user_obj = None
    else:
        user_obj = None

    # If no st.user support, show a fallback sign-in button and explanatory text
    if not user_obj:
        # Fallback minimal UX
        st.warning(
            "This environment doesn't expose `st.user`. Use your app's auth or run on Streamlit Cloud/Enterprise "
            "to enable Google authentication features."
        )
        cols = st.columns([1, 1])
        with cols[0]:
            if st.button("🔓 Simulate Sign In (Demo)"):
                # In demo mode, create a lightweight fake user in session state
                st.session_state["_demo_user"] = {
                    "name": "Demo User",
                    "given_name": "Demo",
                    "email": "demo@example.com",
                    "picture": "https://avatars.dicebear.com/api/identicon/demo.svg",
                    "is_logged_in": True,
                }
                st.experimental_rerun()
        with cols[1]:
            if st.button("❌ Clear Demo User"):
                st.session_state.pop("_demo_user", None)
                st.experimental_rerun()

        # If demo user exists, show profile using that
        demo = st.session_state.get("_demo_user")
        if demo and demo.get("is_logged_in"):
            st.success(GetRandomWelcomeMessage(), icon="🤝")
            st.image(demo.get("picture"), caption=demo.get("name"))
            st.write("Email:", demo.get("email"))
            if st.button("Log out (demo)"):
                st.toast(f"Goodbye, {demo.get('name')}! See you soon!", icon="🚪")
                sleep(1.5)
                st.session_state.pop("_demo_user", None)
                st.experimental_rerun()
        return

    # If we have st.user available from the environment:
    try:
        # st.user typically has fields: is_logged_in, name, given_name, email, picture
        if hasattr(st.user, "is_logged_in") and not st.user.is_logged_in:
            st.title("🔐 Login Required")
            st.write("Please authenticate using your Google account to access your Jarvis profile.")
            if st.button("🔓 Authenticate with Google"):
                # st.login may be provided by Streamlit Enterprise / Cloud
                try:
                    st.login("google")
                except Exception:
                    st.error("Login is not available in this environment.")
        else:
            # Display user profile
            given_name = getattr(st.user, "given_name", None) or getattr(st.user, "name", "there")
            st.title(f"🙏 {GreetUser(given_name)}")
            st.success(GetRandomWelcomeMessage(), icon="🤝")

            # Profile picture
            picture = getattr(st.user, "picture", None)
            if picture:
                st.image(picture, caption=getattr(st.user, "name", ""), width=160)
            else:
                st.info("No profile picture available.")

            st.write("Email:", getattr(st.user, "email", "Not provided"))

            # Example: show last login time if available
            last_login_ts = getattr(st.user, "last_login", None)
            if last_login_ts:
                try:
                    readable = unix_to_ist(last_login_ts)
                    st.write("Last login (IST):", readable)
                except Exception:
                    pass

            if st.button("Log out"):
                st.toast(f"Goodbye, {getattr(st.user, 'name', 'User')}! See you soon!", icon="🚪")
                sleep(1.2)
                try:
                    st.logout()
                except Exception:
                    st.info("Logout hook not available in this environment.")
    except Exception as e:
        st.error(f"An error occurred while accessing user data: {e}")


if __name__ == "__main__":
    auth()
