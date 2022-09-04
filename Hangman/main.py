import random
from english_words import english_words_lower_set

#TODO save/load options
#TODO add GUI

words = list(english_words_lower_set)
used_letters = []
lives = 8


def get_random_word(words: list) -> str:
    return random.choice(words)


def get_user_guess(word: str, guess: str) -> bool:
    return guess in word


def hide_letters(word: str) -> list[str]:
    return ['_' for _ in range(len(word))]

def input_user_guess() -> str:
    while True:
        guess = input('Please enter your letter: ')
        if len(guess) > 1 or len(guess) < 0:
            print('Guess has to be a single letter!')
        elif guess in used_letters:
            print('This letter has been already used!')
        else:
            return guess

def check_complete(hidden_word: list[str]) -> bool:
    return '_' not in hidden_word

def play(lives: int):
    word = get_random_word(words)
    hidden_word = hide_letters(word)
    print(f'The word is {"".join(hidden_word)}')

    while True:
        if lives == 0:
            print(f'You lost! The word was {word}')
            break
        guess = input_user_guess()
        used_letters.append(guess)

        if get_user_guess(word, guess):
            for i in range(len(hidden_word)):
                if word[i] == guess:
                    hidden_word[i] = word[i]
        else:
            print('You lost 1 life!')
            lives -= 1
        print(f'The word is {"".join(hidden_word)}')
        print(f'You have {lives} lives')
        print(f'Used letters: {",".join(used_letters)}')
        if check_complete(hidden_word):
            print('You won!')
            break


def main():
    play(lives)


main()
