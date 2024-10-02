import streamlit as st
import numpy as np
import time
import streamlit_shortcuts
import random

# Grid size
rows = 10
cols = 10
update_interval = 0.5  # Update every 0.5 seconds

# Initial State
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "snake": [(2, 2), (2, 1), (2, 0)],
        "direction": (0, 1),
        "food": (5, 5),
        "score": 0,
        "game_over": False,
        "last_update": time.time(),
        "fruit": "🍐"
    }

def place_food(snake):
    empty_cells = [(r, c) for r in range(rows) for c in range(cols) if (r, c) not in snake]
    return empty_cells[np.random.choice(len(empty_cells))]

def set_fruit(fruits):
    return fruits[random.randint(0, len(fruits)-1)]

def on_button_click():
    if st.session_state.game_state["game_over"]:
        st.session_state.game_state = {
            "snake": [(2, 2), (2, 1), (2, 0)],
            "direction": (0, 1),
            "food": place_food(st.session_state.game_state["snake"]),
            "score": 0,
            "game_over": False,
            "last_update": time.time(),
            "fruit": "🍐"
        }

def update_snake():
    snake = st.session_state.game_state["snake"]
    direction = st.session_state.game_state["direction"]
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if new_head[0] < 0 or new_head[0] >= rows or new_head[1] < 0 or new_head[1] >= cols or new_head in snake:
        st.session_state.game_state["game_over"] = True
        return

    snake.insert(0, new_head)
    if new_head == st.session_state.game_state["food"]:
        st.session_state.game_state["food"] = place_food(snake)
        st.session_state.game_state["fruit"] = set_fruit(["🍎", "🍓", "🍒", "🍊", "🍉"])
        st.session_state.game_state["score"] += 1
    else:
        snake.pop()



def render_grid():
    snake = st.session_state.game_state["snake"]
    food = st.session_state.game_state["food"]
    fruit = st.session_state.game_state["fruit"]

    for row in range(rows):
        columns = st.columns(cols)
        for col_index, col in enumerate(columns):
            with col.container():
                if (row, col_index) == food:
                    col.button(fruit, key=f"button_{row}_{col_index}")
                elif (row, col_index) in snake:
                    col.button("", key=f"button_{row}_{col_index}", type="primary" )
                else:
                    col.button("", key=f"button_{row}_{col_index}", disabled=True)


def control_snake(key):
    if st.session_state.game_state["game_over"]:
        return

    direction_map = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    current_direction = st.session_state.game_state["direction"]
    new_direction = direction_map[key]
    if (current_direction[0] + new_direction[0], current_direction[1] + new_direction[1]) != 0:
        st.session_state.game_state["direction"] = new_direction

def up_callback():
   return control_snake("Up")
def down_callback():
   return control_snake("Down")
def left_callback():
   return control_snake("Left")
def right_callback():
   return control_snake("Right")

# Render game controls and grid
st.title("🐍 Snake Game 🐍")
st.button("Restart Game", on_click=on_button_click)
st.text(f"Score: {st.session_state.game_state['score']}")

st.write("Controls:")
st.write("shift+W > UP | shift+S > DOWN | shift+L > LEFT | shift+R > RIGHT")

# Check the last update time and update snake if the interval has passed.
current_time = time.time()
if current_time - st.session_state.game_state["last_update"] >= update_interval:
    st.session_state.game_state["last_update"] = current_time
    if not st.session_state.game_state["game_over"]:
        update_snake()
    render_grid()
    st.rerun()
else:
    render_grid()

# Control Buttons layout
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        streamlit_shortcuts.button("Up", on_click=up_callback, shortcut="Shift+W")
    with col2:
        streamlit_shortcuts.button("Down", on_click=down_callback, shortcut="Shift+S")
    with col3:
        streamlit_shortcuts.button("Left", on_click=left_callback, shortcut="Shift+A")
    with col4:
        streamlit_shortcuts.button("Right", on_click=right_callback, shortcut="Shift+D")

if st.session_state.game_state["game_over"]:
    st.title("Game Over")
    st.balloons()

# Pause for the update_interval to create a continuous loop effect
time.sleep(update_interval)
if not st.session_state.game_state["game_over"]:
    st.rerun()