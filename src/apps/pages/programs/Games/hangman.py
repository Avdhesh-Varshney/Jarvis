import random
import streamlit as st

HANGMAN_FIGURES = [
    """
      ------
       |    |
       O    |
      /|\\   |
      / \\   |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      /     |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
       |    |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
            |
            |
            |
    =========
    """,
    """
       ------ 
       |    |
            |
            |
            |
            |
    =========
    """,
]  # Hangman figure for every mistake

def get_new_word():
    # Selects a random word from a predefined list of words for the game
    words = ["python", "hangman", "programming", "developer",
            "keyboard", "algorithm", "function", "variable",
            "iteration", "debugging", "constant", "indentation",
            "machine learning", "backend", "frontend", "deep learning",
            "tensorflow", "blockchain", "quantum", "data science"]
    return random.choice(words)

def initialize_game_state():
    # Initializes or resets the game state by defining necessary session variables.
    st.session_state.word = get_new_word()
    st.session_state.guessed_word = ["_"] * len(st.session_state.word)  # Placeholder for guessed letters.
    st.session_state.guessed_letters = set()  # Tracks guessed letters to avoid repeats.
    st.session_state.attempts = 6
    st.session_state.game_over = False
    st.session_state.message = "Welcome to Hangman Game!"
    st.session_state.guess = ""
    st.session_state.play_again_triggered = False
    st.session_state.hint_used = False

def check_guess(guess):
    # Validates the guess and updates the game state accordingly.
    if not guess or len(guess) != 1 or not guess.isalpha():
        return "Please enter a single alphabetic letter."
    if guess in st.session_state.guessed_letters:
        return f"You already guessed '{guess}'. Try a different letter."

    st.session_state.guessed_letters.add(guess)

    if guess in st.session_state.word:
        # Update the guessed word if the letter is correct.
        for i, letter in enumerate(st.session_state.word):
            if letter == guess:
                st.session_state.guessed_word[i] = guess
        return f"Good job! '{guess}' is in the word."
    else:
        st.session_state.attempts -= 1
        return f"Wrong guess! You have {st.session_state.attempts} attempts left."

def give_hint():
    # Provides a hint by revealing a random letter in the word.
    if not st.session_state.hint_used:
        hint_letter = random.choice([letter for letter in st.session_state.word if letter != "_"])
        for i, letter in enumerate(st.session_state.word):
            if letter == hint_letter:
                st.session_state.guessed_word[i] = hint_letter
        st.session_state.hint_used = True
        return f"Here's your hint: The letter '{hint_letter}' is in the word."
    else:
        return "You've already used your hint."

def hangman():
    st.title("Hangman Game")

    if "word" not in st.session_state:
        initialize_game_state()

    st.write(st.session_state.message)  # Displays the current status message.
    st.write("Word:", " ".join(st.session_state.guessed_word))  # Displays the partially guessed word.

    st.code(HANGMAN_FIGURES[st.session_state.attempts], language="text")  # Displays the current hangman figure.

    if not st.session_state.game_over:
        # Text input for guessing a letter.
        st.session_state.guess = st.text_input("Guess a letter:", value=st.session_state.guess, key="guess_input").lower()

        if st.button("Submit Guess"):
            # Process the submitted guess and update the game state.
            st.session_state.message = check_guess(st.session_state.guess)
            st.session_state.guess = ""

            if "_" not in st.session_state.guessed_word:
                # Checks if the entire word has been guessed correctly.
                st.session_state.message = f"\nCongratulations! You've guessed the word correctly: {st.session_state.word}"
                st.session_state.game_over = True
            elif st.session_state.attempts == 0:
                # Ends the game if the player runs out of attempts.
                st.session_state.message = f"\nYou've run out of attempts! The word was: {st.session_state.word}"
                st.session_state.game_over = True

        if st.button("Get a Hint"):
            # Provides a hint to the player.
            hint_message = give_hint()
            st.session_state.message = hint_message

    if st.session_state.game_over:
        # Handles the "Play Again" functionality.
        if st.session_state.play_again_triggered or st.button("Play Again"):
            st.session_state.play_again_triggered = True
            initialize_game_state()
