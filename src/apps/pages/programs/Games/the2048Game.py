import streamlit as st
import numpy as np
import random

def the2048Game():

    def add_new_tile(board):
        """Add a new tile (2 or 4) to a random empty cell"""
        empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            board[i][j] = random.choice([2, 2, 2, 4]) 


    if 'board' not in st.session_state:
        st.session_state.board = np.zeros((4, 4), dtype=int)
        st.session_state.score = 0

        for _ in range(2):
            add_new_tile(st.session_state.board)

    def merge(row):
        """Merge tiles in a row"""
    
        row = [x for x in row if x != 0]
        i = 0
        while i < len(row)-1:
            if row[i] == row[i+1]:
                row[i] *= 2
                st.session_state.score += row[i] 
                row.pop(i+1)  
            i += 1

        return row + [0] * (4 - len(row))

    def move(board, direction):
        """Move tiles in the specified direction"""
        if direction in ['LEFT', 'RIGHT']:
            for i in range(4):
                row = list(board[i, :])
                if direction == 'RIGHT':
                    row.reverse()
                row = merge(row)
                if direction == 'RIGHT':
                    row.reverse()
                board[i, :] = row
        else:  
            for j in range(4):
                col = list(board[:, j])
                if direction == 'DOWN':
                    col.reverse()
                col = merge(col)
                if direction == 'DOWN':
                    col.reverse()
                board[:, j] = col
        return board


    st.markdown(
        """
        <h1 style='text-align: center; padding-top: 50px; padding-bottom: 50px; font-size: 100px;'>
            2️⃣0️⃣4️⃣8️⃣ 
        </h1>
        """,
        unsafe_allow_html=True
    )

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

    for i in range(4):
        cols = st.columns(4)
        for j in range(4):
            value = st.session_state.board[i][j]
            bg_color = color_dict.get(value, '#CDC1B4')
            text_color = '#776E65' if value in [2, 4] else '#F9F6F2'
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
            


    left_space, control_area, right_space = st.columns([2, 1, 2])

    st.markdown("""
        <style>
            /* New Game button style - match score size exactly */
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

            /* Arrow buttons style - transparent */
            div[data-testid="stButton"] button[kind="secondary"] {
                font-size: 36px !important;
                font-weight: bold !important;
                padding: 15px 25px !important;
                border-radius: 8px !important;
                background-color: rgba(255, 255, 255, 0.1) !important;
                color: white !important;
                border: 2px solid rgba(255, 255, 255, 0.5) !important;
                margin: 5px !important;
                width: 70px !important;
                height: 70px !important;
                line-height: 40px !important;
                transition: all 0.3s !important;
            }
            div[data-testid="stButton"] button[kind="secondary"]:hover {
                background-color: rgba(255, 255, 255, 0.2) !important;
                border-color: rgba(255, 255, 255, 0.8) !important;
            }

            /* Center content in columns */
            div[data-testid="column"] {
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                padding: 0px !important;
            }
        </style>
    """, unsafe_allow_html=True)


    if st.button('New Game', type='primary'):
        st.session_state.board = np.zeros((4, 4), dtype=int)
        st.session_state.score = 0
        for _ in range(2):
            add_new_tile(st.session_state.board)
        st.rerun()


    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)


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

        if any(0 in row for row in st.session_state.board):
            return False
        

        for i in range(4):
            for j in range(3):
                if st.session_state.board[i][j] == st.session_state.board[i][j + 1]:
                    return False
                if st.session_state.board[j][i] == st.session_state.board[j + 1][i]:
                    return False
        return True

    if is_game_over():
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
        old_board = st.session_state.board.copy()
        st.session_state.board = move(st.session_state.board, direction)
        if not np.array_equal(old_board, st.session_state.board):
            add_new_tile(st.session_state.board)
