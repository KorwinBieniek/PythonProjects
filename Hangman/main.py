import random

words = ['key', 'horse', 'motor', 'car', 'home', 'mountain']


def get_random_word(words: list) -> str:
    return random.choice(words)


def get_user_guess(word: str, guess: str) -> bool:
    return guess in word


def hide_letters(word: str) -> list[str]:
    return ['_' for _ in range(len(word))]


def play():
    word = get_random_word(words)
    hidden_word = hide_letters(word)
    print(f'The word is {"".join(hidden_word)}')
    while True:
        guess = input('Please enter your letter: ')
        if get_user_guess(word, guess):
            for i in range(len(hidden_word)):
                if word[i] == guess:
                    hidden_word[i] = word[i]
            print(f'The word is {"".join(hidden_word)}')


def main():
    play()


main()
