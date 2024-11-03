import streamlit as st
import numpy as np
import random

# Function to check rows for a winner
def checkRows(board):
    for row in board:
        if len(set(row)) == 1 and row[0] != ".":
            return row[0]
    return None

# Function to check diagonals for a winner
def checkDiagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1 and board[0][0] != ".":
        return board[0][0]
    if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1 and board[0][len(board) - 1] != ".":
        return board[0][len(board) - 1]
    return None

# Function to check if there is a winner
def checkWin(board):
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard)
        if result:
            return result
    return checkDiagonals(board)

# Function to check if the board is full
def checkDraw(board):
    return not any("." in row for row in board)

# Function to randomly decide who starts the game
def decide_start():
    return random.choice(["player", "jarvis"])

# Function for Jarvis to make a move
def jarvis_move():
    if not st.session_state.winner and not st.session_state.draw:
        # Simulate Jarvis's move
        empty_cells = [(i, j) for i in range(3) for j in range(3) if st.session_state.board[i, j] == "."]
        if empty_cells:
            i, j = random.choice(empty_cells)
            st.session_state.board[i, j] = st.session_state.jarvis_symbol
            winner = checkWin(st.session_state.board)
            if winner:
                st.session_state.winner = winner
            elif checkDraw(st.session_state.board):
                st.session_state.draw = True
            else:
                st.session_state.current_turn = "player"
                st.session_state.next_player = st.session_state.player_symbol

# Main Tic Tac Toe game function
def ticTacToe():
    st.title("🎮 Tic Tac Toe Game 🎮")

    def initialize_game():
        st.session_state.board = np.full((3, 3), ".", dtype=str)
        st.session_state.winner = None
        st.session_state.draw = False

        # Randomly assign symbols to player and Jarvis
        symbols = ["X", "O"]
        random.shuffle(symbols)
        st.session_state.player_symbol = symbols[0]
        st.session_state.jarvis_symbol = symbols[1]

        # Randomly decide who starts
        st.session_state.current_turn = decide_start()
        if st.session_state.current_turn == "player":
            st.session_state.next_player = st.session_state.player_symbol
        else:
            st.session_state.next_player = st.session_state.jarvis_symbol
            jarvis_move()

    # Initialize board and game state in Streamlit session state if not already initialized
    if "board" not in st.session_state:
        initialize_game()

    # Function to handle button click and game logic
    def handle_click(i, j):
        if not st.session_state.winner and not st.session_state.draw and st.session_state.board[i, j] == ".":
            st.session_state.board[i, j] = st.session_state.next_player
            winner = checkWin(st.session_state.board)
            if winner:
                st.session_state.winner = winner
            elif checkDraw(st.session_state.board):
                st.session_state.draw = True
            else:
                if st.session_state.current_turn == "player":
                    st.session_state.current_turn = "jarvis"
                    st.session_state.next_player = st.session_state.jarvis_symbol
                    jarvis_move()
                else:
                    st.session_state.current_turn = "player"
                    st.session_state.next_player = st.session_state.player_symbol

    # Display player symbols outside the game area
    st.write(f"You: {st.session_state.player_symbol} | Jarvis: {st.session_state.jarvis_symbol}")

    # Display the Tic Tac Toe board with enhanced UI elements
    with st.container():
        st.subheader("Tic Tac Toe Board")
        for i, row in enumerate(st.session_state.board):
            cols = st.columns(3)
            for j, field in enumerate(row):
                if field == ".":
                    cols[j].button(
                        label=" ",
                        key=f"{i}-{j}",
                        on_click=handle_click,
                        args=(i, j),
                        help="Click to mark this position",
                    )
                else:
                    cols[j].button(
                        label=field,
                        key=f"{i}-{j}",
                        on_click=handle_click,
                        args=(i, j),
                        help="Click to mark this position",
                        disabled=True,
                    )

        # Display current player and winner message
        st.write("")
        st.subheader("Game Status")
        if st.session_state.winner:
            st.success(f"🎉 Congratulations! {st.session_state.winner} won the game! 🎉")
        elif st.session_state.draw:
            st.warning("It's a draw! 🤝")
        else:
            turn_message = "Your turn" if st.session_state.current_turn == "player" else "Jarvis's turn"
            st.write(turn_message)

    # button to restart the game
    if st.button("Restart Game"):
        initialize_game()
