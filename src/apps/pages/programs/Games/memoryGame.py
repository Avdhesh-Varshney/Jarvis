import streamlit as st
import random

def memoryGame():
    # Center the title with padding using custom HTML
    st.markdown(
        """
        <h1 style='text-align: center; padding-top: 50px; padding-bottom: 50px; font-size: 60px;'>
            🧠 Memory Game 🧠
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Game settings
    GRID_SIZE = 4  # 4x4 grid
    NUM_PAIRS = (GRID_SIZE * GRID_SIZE) // 2

    # Initialize game state
    if "moves" not in st.session_state:
        st.session_state.moves = 0
    if "best_score" not in st.session_state:
        st.session_state.best_score = float('inf')  # Use infinity as the initial best score
    if "matches_found" not in st.session_state:
        st.session_state.matches_found = 0

    # Initialize session state variables
    if 'numbers' not in st.session_state:
        # Create pairs of numbers and shuffle them
        numbers = list(range(1, NUM_PAIRS + 1)) * 2
        random.shuffle(numbers)
        st.session_state.numbers = numbers
        st.session_state.revealed = [False] * len(numbers)
        st.session_state.first_selection = None
        st.session_state.second_selection = None
        st.session_state.moves = 0
        st.session_state.matches_found = 0

    # Game logic functions
    def handle_card_click(index):
        """Handle the card click."""
        if st.session_state.revealed[index]:
            return  # Ignore if the card is already revealed

        # If the first selection is empty, set it to the current index
        if st.session_state.first_selection is None:
            st.session_state.first_selection = index
        # If the second selection is empty, set it to the current index
        elif st.session_state.second_selection is None:
            st.session_state.second_selection = index
            st.session_state.moves += 1
            
            # Disable buttons to prevent further clicks until the check is done
            st.session_state.disable_buttons = True
            
            # Check if the cards match
            check_match()
            
        # Ensure that we only select two cards at a time
        if st.session_state.first_selection is not None and st.session_state.second_selection is not None:
            # Optionally, you could add a mechanism to delay the checking or visual feedback here
            st.session_state.disable_buttons = False  # Re-enable buttons after processing

    def check_match():
        """Check if the two selected cards match."""
        first_idx = st.session_state.first_selection
        second_idx = st.session_state.second_selection
        
        # Check if the selected cards match
        if st.session_state.numbers[first_idx] == st.session_state.numbers[second_idx]:
            st.session_state.revealed[first_idx] = True
            st.session_state.revealed[second_idx] = True
            st.session_state.matches_found += 1

        # Reset selections
        st.session_state.first_selection = None
        st.session_state.second_selection = None
        
        # Re-enable the buttons
        st.session_state.disable_buttons = False

    # Add custom CSS to change the button size
    button_style = """
        <style>
        .stButton>button {
            width: 100px;
            height: 100px;
            font-size: 24px;
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # Display the grid of cards
    cols = st.columns(GRID_SIZE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            idx = i * GRID_SIZE + j
            if st.session_state.revealed[idx] or st.session_state.first_selection == idx or st.session_state.second_selection == idx:
                # Show the number if the card is revealed or currently selected
                cols[j].button(str(st.session_state.numbers[idx]), key=idx, disabled=True)
            else:
                # Show a blank button if the card is not revealed
                if cols[j].button("?", key=idx):
                    handle_card_click(idx)

    # Display game information in separate columns
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Best:** {int(st.session_state.best_score) if st.session_state.best_score != float('inf') else 'N/A'}")

    with col2:
        st.write(f"**Moves:** {st.session_state.moves}")

    # Add the following function to generate confetti
    def add_confetti():
        st.markdown(
            """
            <script src="https://cdnjs.cloudflare.com/ajax/libs/canvas-confetti/1.4.0/confetti.browser.min.js"></script>
            <script>
                var count = 200;
                var defaults = {
                    origin: { y: 0.7 }
                };

                function fire(particleRatio, opts) {
                    confetti(Object.assign({}, defaults, opts, {
                        particleCount: Math.floor(count * particleRatio)
                    }));
                }

                fire(0.25, { spread: 26, startVelocity: 55 });
                fire(0.2, { spread: 60 });
                fire(0.35, { spread: 100, decay: 0.91, scalar: 1.2 });
                fire(0.15, { spread: 120, startVelocity: 30, decay: 0.92 });
                fire(0.1, { spread: 180, startVelocity: 50 });
            </script>
            """,
            unsafe_allow_html=True
        )

    # Check if the player has won
    if st.session_state.matches_found == NUM_PAIRS:
        add_confetti()  # Add confetti effect
        st.markdown("<h1 style='text-align: center; font-size: 48px; color: #4CAF50;'>Congratulations, you won!</h1>", unsafe_allow_html=True)

        # Update best score
        if st.session_state.moves < st.session_state.best_score:
            st.session_state.best_score = st.session_state.moves

    # Add a reset button
    if st.button("Restart Game"):
        # Reset session state variables
        numbers = list(range(1, NUM_PAIRS + 1)) * 2
        random.shuffle(numbers)
        st.session_state.numbers = numbers
        st.session_state.revealed = [False] * len(numbers)
        st.session_state.first_selection = None
        st.session_state.second_selection = None
        st.session_state.moves = 0
        st.session_state.matches_found = 0