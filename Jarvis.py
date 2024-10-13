from database.mongodb import create_connection, login_user
from database.localStorageServer import server
from datetime import datetime, timedelta
import streamlit as st
import pygame
import time
import random

# Initialize Pygame for the Snake game
pygame.init()

# Define the size of the game window for Snake
window_x = 720
window_y = 480

# Define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Set up game window
game_window = pygame.display.set_mode((window_x, window_y))

# Frames per second controller
fps = pygame.time.Clock()

# Snake default position and body
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# Food position and spawn flag
food_position = [random.randrange(1, (window_x // 10)) * 10,
                 random.randrange(1, (window_y // 10)) * 10]
food_spawn = True

# Snake's initial direction and score
direction = 'RIGHT'
score = 0

# Snake Game Logic
def snake_game():
    global snake_position, snake_body, food_position, food_spawn, direction, score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        # Spawning food
        if not food_spawn:
            food_position = [random.randrange(1, (window_x // 10)) * 10,
                             random.randrange(1, (window_y // 10)) * 10]
        food_spawn = True

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x - 10 or snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over()
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        # Fill the background
        game_window.fill(black)

        # Draw the snake
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw the food
        pygame.draw.rect(game_window, white, pygame.Rect(food_position[0], food_position[1], 10, 10))

        # Display the score
        show_score(1, white, 'times new roman', 20)

        # Refresh game screen
        pygame.display.update()

        # Set the speed of the snake
        fps.tick(15)

# Game Over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Show score function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (window_x / 10, 15)
    else:
        score_rect.midtop = (window_x / 2, window_y / 1.25)
    game_window.blit(score_surface, score_rect)

# Streamlit session and state handling
today = datetime.now()

if "user" not in st.session_state:
    st.session_state['password'] = None
    st.session_state["user"] = ['', '', '', '', '', '', '', '']
    st.session_state['expiration_date'] = (today - timedelta(days=10)).isoformat()
    st.session_state['verified'] = False

# Function to get credentials from local storage
def getCredentials():
    conn = server()
    return conn.getLocalStorageVal("password"), conn.getLocalStorageVal("user"), conn.getLocalStorageVal("expiration_date"), conn.getLocalStorageVal("verified")

# Logged-in state management
def logged_in():
    from src.auth.login import login
    userData, password, remember_me = login()

    if userData != []:
        conn = server()
        user = [userData['username'], userData['email'], userData['first_name'], userData['last_name'], userData['role'], userData['gender'], userData['age'], userData['about']]

        conn.setLocalStorageVal("user", user)
        conn.setLocalStorageVal("password", password)
        conn.setLocalStorageVal("expiration_date", (today + timedelta(days=(30 if remember_me else 1))).isoformat())
        conn.setLocalStorageVal("verified", True)
        st.info("Please refresh the page to continue", icon="ℹ️")

# Main app structure and navigation
def application():
    # Public pages
    home = st.Page("src/apps/public/home.py", title="Home", icon=":material/home:")
    youtubePlaylist = st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:")

    # Authentication pages
    login_page = st.Page(logged_in, title="Log in", icon=":material/login:")
    sign_up_page = st.Page("src/auth/signup.py", title="Sign up", icon=":material/person_add:")

    # Game section: Add Snake Game
    if st.sidebar.button('Play Snake Game'):
        st.write("Launching Snake Game...")
        snake_game()

    # Return the navigation structure
    return st.navigation({
        "": [home, youtubePlaylist], 
        "Account": [login_page, sign_up_page],
        "Games": [snake_game]  # Added Snake Game under Games section
    })

# Main execution
if __name__ == "__main__":
    app = application()

    if st.session_state['password'] is None:
        st.session_state['password'], st.session_state['user'], st.session_state['expiration_date'], st.session_state['verified'] = getCredentials()

    if st.session_state['password'] is not None and st.session_state['expiration_date'] > today.isoformat():
        if not st.session_state['verified']:
            conn = create_connection()
            result = login_user(conn, st.session_state['user'].split(',')[0], st.session_state['password'])
            if result:
                st.session_state['verified'] = True
                conn = server()
                conn.setLocalStorageVal("verified", True)
        if st.session_state['verified']:
            from src.utils.functions import load_functions
            app = st.navigation(pages=load_functions())

    app.run()
