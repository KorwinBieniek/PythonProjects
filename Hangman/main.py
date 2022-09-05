import random
import pygame
from english_words import english_words_lower_set


# TODO add GUI

WIN = pygame.display.set_mode([500, 500])
pygame.font.init()
FONT = pygame.font.Font('freesansbold.ttf', 28)
pygame.display.set_caption('Hangman')


words = list(english_words_lower_set)
used_letters = []
lives = 10

def get_random_word(words: list) -> str:
    return random.choice(words)


def get_user_guess(word: str, guess: str) -> bool:
    return guess in word


def hide_letters(word: str) -> list[str]:
    return ['_' for _ in range(len(word))]


def input_user_guess(word: str, hidden_word: list[str], used_letters: list[str], lives: int) -> str:
    while True:

        guess = input('Please enter your letter: ')
        if guess == 'save':
            save_game('game.txt', word, hidden_word, used_letters, lives)
        elif guess == 'exit':
            exit(0)
        elif len(guess) > 1 or len(guess) < 0:
            print('Guess has to be a single letter!')
        elif guess in used_letters:
            print('This letter has been already used!')
        else:
            return guess


def check_complete(hidden_word: list[str]) -> bool:
    return '_' not in hidden_word


def play(lives: int, word: str, used_letters: list[str], hidden_word: list[str]):
    pygame.init()
    running = True

    while running:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        WIN.fill((255, 255, 255))


        text_surface = FONT.render(f'Lives: {lives}', True, (0, 0, 0))
        WIN.blit(text_surface, (12, 12))

        text_surface = FONT.render(f'Word: {" ".join(hidden_word)}', True, (0, 0, 0))
        WIN.blit(text_surface, (75, 50))

        text_surface = FONT.render(f'Used Letters: {", ".join(used_letters)}', True, (0, 0, 0))
        WIN.blit(text_surface, (10, 450))

        img = pygame.image.load(f'images/{abs(lives - 10)}.jpg')
        WIN.blit(img, (250, 100))
        pygame.display.flip()

        # load = input('Would you like to load last game? yes/no: ')
        # if load == 'yes':
        #     unpack = load_game('game.txt').split()
        #     lives = int(unpack[0])
        #     word = unpack[1]
        #     used_letters = unpack[2].split('|')
        #     hidden_word = list(unpack[3])
        #TODO naprawic loading

        if lives == 0:
            print(f'You lost! The word was {word}')
            break
        guess = input_user_guess(word, hidden_word, used_letters, lives)
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

        pygame.display.update()
    pygame.quit()






    # print(f'The word is {"".join(hidden_word)}')
    # print(f'You have {lives} lives')
    # print(f'Used letters: {",".join(used_letters)}')
    #



def main():
    word = get_random_word(words)
    hidden_word = hide_letters(word)
    play(lives, word, used_letters, hidden_word)


def save_game(filename, word, hidden_word, used_letters, lives):
    with open(filename, 'w') as file:
        file.write(f'{lives} {word} {"|".join(used_letters)} {"".join(hidden_word)}')


def load_game(filename):
    with open(filename, 'r') as file:
        return file.read()


main()
