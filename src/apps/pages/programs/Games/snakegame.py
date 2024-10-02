import streamlit as st
import numpy as np
import random
import time

# Define grid size and directions
GRID_SIZE = 20
directions = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}

# Initialize game state
def initialize_game():
    st.session_state.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
    st.session_state.food = place_food(st.session_state.snake)
    st.session_state.direction = "RIGHT"
    st.session_state.alive = True
    st.session_state.score = 0

# Place food on the grid
def place_food(snake):
    while True:
        food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if food not in snake:
            return food

# Move the snake and update the game state
def move_snake():
    if not st.session_state.alive:
        return

    # Calculate new head position
    head_x, head_y = st.session_state.snake[0]
    dir_x, dir_y = directions[st.session_state.direction]
    new_head = (head_x + dir_x, head_y + dir_y)

    # Check for collisions
    if (
        new_head[0] < 0 or new_head[0] >= GRID_SIZE or
        new_head[1] < 0 or new_head[1] >= GRID_SIZE or
        new_head in st.session_state.snake
    ):
        st.session_state.alive = False
        return

    # Move the snake
    st.session_state.snake = [new_head] + st.session_state.snake[:-1]

    # Check if food is eaten
    if new_head == st.session_state.food:
        st.session_state.snake.append(st.session_state.snake[-1])  # Grow the snake
        st.session_state.food = place_food(st.session_state.snake)
        st.session_state.score += 1

# Display the game grid
def display_grid():
    grid = np.full((GRID_SIZE, GRID_SIZE), " ")
    for x, y in st.session_state.snake:
        grid[x, y] = "🟩"
    food_x, food_y = st.session_state.food
    grid[food_x, food_y] = "🍎"
    st.write("\n".join([" ".join(row) for row in grid]))

# Handle key presses for direction
def handle_keypress(key):
    if key == "w" and st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
    elif key == "s" and st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"
    elif key == "a" and st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
    elif key == "d" and st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"

# Main Snake Game function
def snake_game():
    st.title("🐍 Snake Game 🐍")
    
    # Initialize game state if not already done
    if "snake" not in st.session_state:
        initialize_game()

    # Capture keyboard input
    st.text("Use W (up), A (left), S (down), D (right) keys to control the snake")
    for key in ["w", "a", "s", "d"]:
        if st.button(f"{key.upper()}", key=key):
            handle_keypress(key)

    # Move the snake
    move_snake()

    # Display the grid
    display_grid()

    # Display game status
    if not st.session_state.alive:
        st.error(f"Game Over! Your Score: {st.session_state.score}")
    else:
        st.success(f"Score: {st.session_state.score}")

    # Restart the game
    if st.button("Restart Game"):
        initialize_game()

# Run the game
snake_game()
