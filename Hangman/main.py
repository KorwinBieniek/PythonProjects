import random

words = ['key', 'horse', 'motor', 'car', 'home', 'mountain']
used_letters = []


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

def play():
    word = get_random_word(words)
    hidden_word = hide_letters(word)
    print(f'The word is {"".join(hidden_word)}')
    while True:
        guess = input_user_guess()
        used_letters.append(guess)
        if get_user_guess(word, guess):
            for i in range(len(hidden_word)):
                if word[i] == guess:
                    hidden_word[i] = word[i]
            print(f'The word is {"".join(hidden_word)}')
        if check_complete(hidden_word):
            print('You won!')
            break


def main():
    play()


main()
