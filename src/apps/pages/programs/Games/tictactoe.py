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

# Main Tic Tac Toe game function
def tictactoe():
    st.title("🎮 Streamlit Tic Tac Toe Game 🎮")

    # Initialize board and game state in Streamlit session state
    if "board" not in st.session_state:
        st.session_state.board = np.full((3, 3), ".", dtype=str)
        st.session_state.next_player = "X"
        st.session_state.winner = None

        # Randomly assign symbols to player and Jarvis
        symbols = ["X", "O"]
        random.shuffle(symbols)
        st.session_state.player_symbol = symbols[0]
        st.session_state.jarvis_symbol = symbols[1]

    # Function to handle button click and game logic
    def handle_click(i, j):
        if not st.session_state.winner and st.session_state.board[i, j] == ".":
            st.session_state.board[i, j] = st.session_state.next_player
            st.session_state.next_player = st.session_state.jarvis_symbol if st.session_state.next_player == st.session_state.player_symbol else st.session_state.player_symbol
            winner = checkWin(st.session_state.board)
            if winner:
                st.session_state.winner = winner
            else:
                # Jarvis makes a move
                jarvis_move()

    # Function for Jarvis to make a move
    def jarvis_move():
        if not st.session_state.winner:
            # Simulate Jarvis's move - you can modify this logic for smarter AI
            empty_cells = [(i, j) for i in range(3) for j in range(3) if st.session_state.board[i, j] == "."]
            if empty_cells:
                i, j = random.choice(empty_cells)
                st.session_state.board[i, j] = st.session_state.jarvis_symbol
                st.session_state.next_player = st.session_state.player_symbol
                winner = checkWin(st.session_state.board)
                if winner:
                    st.session_state.winner = winner

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
        else:
            st.write(f"Next Player: {st.session_state.next_player}")

# Run the Tic Tac Toe game if this script is executed directly
if __name__ == "__main__":
    tictactoe()
