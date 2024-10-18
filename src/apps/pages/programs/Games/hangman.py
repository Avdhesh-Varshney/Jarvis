import streamlit as st
import random
import string

def load_words():
    return [
        "algorithm", "backend", "blockchain", "cryptography", "debugging",
        "encryption", "framework", "middleware", "optimization", "parallelism",
        "quantum", "refactoring", "scalability", "virtualization", "kubernetes",
        "tensorflow", "microservices", "serverless", "neural network", "machine learning",
        "data science", "bioinformatics", "cybersecurity", "devops", "distributed systems"
    ]

def choose_word(words):
    return random.choice(words)

def get_hanging_message(mistakes):
    messages = [
        "The noose is ready...",
        "20% HANGED - Head is placed",
        "40% HANGED - Body is hung",
        "60% HANGED - One arm is tied",
        "80% HANGED - Both arms are tied",
        "MAN IS DEAD - Game Over!"
    ]
    return messages[mistakes]

def initialize_game_state():
    if 'word' not in st.session_state:
        st.session_state.word = choose_word(load_words())
        st.session_state.word_letters = set(st.session_state.word.replace(" ", ""))
        st.session_state.used_letters = set()
        st.session_state.lives = 5
        st.session_state.mistakes = 0
        st.session_state.hint_given = False

def main():
    st.title("Technical Hangman Game")
    st.write("Can you guess the technical term before the man is hanged?")

    initialize_game_state()

    # Display game state
    st.write(f"Lives left: {st.session_state.lives}")
    st.write("Used letters: " + " ".join(sorted(st.session_state.used_letters)))
    
    word_display = " ".join([letter if letter in st.session_state.used_letters or letter == " " else "_" for letter in st.session_state.word])
    st.write("Current word:", word_display)

    st.write(get_hanging_message(st.session_state.mistakes))

    # Get user input
    user_letter = st.text_input("Guess a letter:", max_chars=1).lower()

    if st.button("Submit Guess"):
        if user_letter:
            if user_letter in string.ascii_lowercase and user_letter not in st.session_state.used_letters:
                st.session_state.used_letters.add(user_letter)
                if user_letter in st.session_state.word_letters:
                    st.session_state.word_letters.remove(user_letter)
                    st.success("Good guess!")
                else:
                    st.session_state.lives -= 1
                    st.session_state.mistakes += 1
                    st.error("Wrong guess. You lose a life.")
            elif user_letter in st.session_state.used_letters:
                st.warning("You've already guessed that letter. Try again.")
            else:
                st.warning("Invalid character. Please enter a single letter.")

        # Give a hint if the player is struggling
        if st.session_state.lives == 2 and len(st.session_state.word_letters) > len(st.session_state.word) / 2 and not st.session_state.hint_given:
            hint_letter = random.choice(list(st.session_state.word_letters))
            st.info(f"Hint: The word contains the letter '{hint_letter}'")
            st.session_state.used_letters.add(hint_letter)
            st.session_state.word_letters.remove(hint_letter)
            st.session_state.hint_given = True

        # Check game end conditions
        if st.session_state.lives == 0:
            st.error(f"Game Over! The man is hanged. The word was '{st.session_state.word}'.")
            if st.button("Play Again"):
                initialize_game_state()
                st.experimental_rerun()
        elif len(st.session_state.word_letters) == 0:
            st.success(f"Congratulations! You guessed the word '{st.session_state.word}'!")
            st.balloons()
            if st.button("Play Again"):
                initialize_game_state()
                st.experimental_rerun()

if __name__ == "__main__":
    main()
