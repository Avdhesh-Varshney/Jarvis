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

def hangman():
    words = load_words()
    word = choose_word(words)
    word_letters = set(word.replace(" ", ""))  # Remove spaces for checking
    alphabet = set(string.ascii_lowercase)
    used_letters = set()

    lives = 5
    mistakes = 0

    print("\nWelcome to the Technical Hangman Game!")
    print("Can you guess the technical term before the man is hanged?")
    print(get_hanging_message(mistakes))

    while len(word_letters) > 0 and lives > 0:
        print(f"\nYou have {lives} lives left.")
        print("Used letters:", " ".join(sorted(used_letters)))

        word_list = [letter if letter in used_letters or letter == " " else "_" for letter in word]
        print("Current word:", " ".join(word_list))

        user_letter = input("Guess a letter: ").lower()
        if len(user_letter) == 1 and user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print("Good guess!")
            else:
                lives -= 1
                mistakes += 1
                print("Wrong guess. You lose a life.")
                print(get_hanging_message(mistakes))
        elif user_letter in used_letters:
            print("You've already guessed that letter. Try again.")
        else:
            print("Invalid character. Please enter a single letter.")

        # Give a hint if the player is struggling
        if lives == 2 and len(word_letters) > len(word) / 2:
            hint_letter = random.choice(list(word_letters))
            print(f"Hint: The word contains the letter '{hint_letter}'")
            used_letters.add(hint_letter)
            word_letters.remove(hint_letter)

    if lives == 0:
        print(f"\nGame Over! The man is hanged. The word was '{word}'.")
    else:
        print(f"\nCongratulations! You guessed the word '{word}'!")
        print("You saved the man from being hanged!")

if __name__ == "__main__":
    hangman()