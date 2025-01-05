import streamlit as st
import numpy as np
import random

def the2048Game():

    def add_new_tile(board):
        """Add a new tile (2 or 4) to a random empty cell"""
        empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            board[i][j] = random.choice([2, 2, 2, 4])  # Randomly assign 2 or 4 to an empty cell

    # Initialize the game state if not already present in session
    if 'board' not in st.session_state:
        st.session_state.board = np.zeros((4, 4), dtype=int)  # 4x4 board initialized with zeros
        st.session_state.score = 0  # Initialize score

        # Add two starting tiles
        for _ in range(2):
            add_new_tile(st.session_state.board)

    def merge(row):
        """Merge tiles in a row, merging same-valued adjacent tiles"""
        row = [x for x in row if x != 0]  # Remove zeros
        i = 0
        while i < len(row)-1:
            if row[i] == row[i+1]:  # If two adjacent tiles are equal
                row[i] *= 2  # Double the value
                st.session_state.score += row[i]  # Update score
                row.pop(i+1)  # Remove the merged tile
            i += 1

        return row + [0] * (4 - len(row))  # Add zeros to the end of the row to maintain size

    def move(board, direction):
        """Move tiles in the specified direction (LEFT, RIGHT, UP, DOWN)"""
        if direction in ['LEFT', 'RIGHT']:
            for i in range(4):
                row = list(board[i, :])  # Get row
                if direction == 'RIGHT':
                    row.reverse()  # Reverse row for right movement
                row = merge(row)  # Merge tiles in the row
                if direction == 'RIGHT':
                    row.reverse()  # Reverse back after merging
                board[i, :] = row  # Update row on the board
        else:  # Move up/down
            for j in range(4):
                col = list(board[:, j])  # Get column
                if direction == 'DOWN':
                    col.reverse()  # Reverse column for down movement
                col = merge(col)  # Merge tiles in the column
                if direction == 'DOWN':
                    col.reverse()  # Reverse back after merging
                board[:, j] = col  # Update column on the board
        return board

    # Display game title
    st.markdown(
        """
        <h1 style='text-align: center; padding-top: 50px; padding-bottom: 50px; font-size: 100px;'>
            2️⃣0️⃣4️⃣8️⃣ 
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Display current score
    st.markdown(f"""
        <div style='
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin: 20px 0;
            text-align: left;
            border: 3px solid white;
            border-radius: 10px;
            padding: 10px 20px;
            display: inline-block;
            background-color: rgba(255, 255, 255, 0.1);
        '>
            Score: {st.session_state.score}
        </div>
    """, unsafe_allow_html=True)

    # Color dictionary for tile values
    color_dict = {
        0: '#CDC1B4',
        2: '#EEE4DA',
        4: '#EDE0C8',
        8: '#F2B179',
        16: '#F59563',
        32: '#F67C5F',
        64: '#F65E3B',
        128: '#EDCF72',
        256: '#EDCC61',
        512: '#EDC850',
        1024: '#EDC53F',
        2048: '#EDC22E'
    }

    # Display the game board
    for i in range(4):
        cols = st.columns(4)
        for j in range(4):
            value = st.session_state.board[i][j]
            bg_color = color_dict.get(value, '#CDC1B4')  # Get background color for tile
            text_color = '#776E65' if value in [2, 4] else '#F9F6F2'  # Light text for low values
            cols[j].markdown(
                f"""
                <div style='
                    background-color: {bg_color};
                    aspect-ratio: 1;
                    text-align: center;
                    font-size: 50px;
                    font-weight: bold;
                    color: {text_color};
                    border-radius: 5px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 5px 0px;
                '>
                    {value if value != 0 else ''}
                </div>
                """,
                unsafe_allow_html=True
            )

    # Display New Game button with custom style
    left_space, control_area, right_space = st.columns([2, 1, 2])

    st.markdown("""
        <style>
            /* New Game button style */
            div[data-testid="stButton"] button[kind="primary"] {
                font-size: 36px !important;
                font-weight: bold !important;
                padding: 10px 20px !important;
                border-radius: 10px !important;
                background-color: rgba(255, 255, 255, 0.1) !important;
                color: white !important;
                border: 3px solid white !important;
                margin: 20px 0 !important;
                width: 200px !important;
                height: 70px !important;
                line-height: normal !important;
                transition: background-color 0.3s !important;
            }
            div[data-testid="stButton"] button[kind="primary"]:hover {
                background-color: rgba(255, 255, 255, 0.2) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    if st.button('New Game', type='primary'):
        """Reset the game state and start a new game"""
        st.session_state.board = np.zeros((4, 4), dtype=int)
        st.session_state.score = 0
        for _ in range(2):
            add_new_tile(st.session_state.board)
        st.rerun()

    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

    # Control buttons for the game (arrow keys)
    left_space, control_area, right_space = st.columns([2, 3, 2])

    with control_area:
        col1, col2, col3 = st.columns([1.2, 1, 1.2])
        col2.button('↑', key='up', type='secondary', on_click=lambda: move_and_update('UP'))

        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown("<div style='padding: 0 10px;'>", unsafe_allow_html=True)
            st.button('←', key='left', type='secondary', on_click=lambda: move_and_update('LEFT'))
        with col2:
            st.markdown("<div style='padding: 0 10px;'>", unsafe_allow_html=True)
            st.button('↓', key='down', type='secondary', on_click=lambda: move_and_update('DOWN'))
        with col3:
            st.markdown("<div style='padding: 0 10px;'>", unsafe_allow_html=True)
            st.button('→', key='right', type='secondary', on_click=lambda: move_and_update('RIGHT'))

    def is_game_over():
        """Check if there are any valid moves left"""
        if any(0 in row for row in st.session_state.board):  # If there's any empty cell
            return False
        
        # Check if there are any adjacent cells with the same value
        for i in range(4):
            for j in range(3):
                if st.session_state.board[i][j] == st.session_state.board[i][j + 1]:
                    return False
                if st.session_state.board[j][i] == st.session_state.board[j + 1][i]:
                    return False
        return True

    if is_game_over():
        """Display Game Over message and score"""
        st.markdown("""
            <div style='
                background-color: rgba(0, 0, 0, 0.7);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
                font-size: 24px;
                font-weight: bold;
            '>
                Game Over!<br>
                Final Score: {score}
            </div>
        """.format(score=st.session_state.score), unsafe_allow_html=True)

    def move_and_update(direction):
        """Update the board after a move"""
        old_board = st.session_state.board.copy()
        st.session_state.board = move(st.session_state.board, direction)  # Move the tiles
        if not np.array_equal(old_board, st.session_state.board):  # Check if the board changed
            add_new_tile(st.session_state.board)  # Add a new tile if the board changed
