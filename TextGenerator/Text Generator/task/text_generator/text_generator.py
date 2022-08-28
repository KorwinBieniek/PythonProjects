import random

from nltk.tokenize import WhitespaceTokenizer
from nltk.util import ngrams


def open_file():
    filename = input('Please input a filename: ')
    return open(filename, 'r', encoding='utf-8')


def create_trigrams(f):
    tokenizer = WhitespaceTokenizer()
    file_text = f.read()
    tokens = tokenizer.tokenize(file_text)
    trigrams_tuple = ngrams(tokens, 3)
    trigrams_list = []
    for first, second, third in trigrams_tuple:
        string_pair = (first + ' ' + second, third)
        trigrams_list.append(string_pair)

    return trigrams_list


def count_tail_occurrences(trigram_list, word):
    dict_of_words = {}
    for words in trigram_list:
        if words[0] == word:
            if words[1] in dict_of_words:
                dict_of_words[words[1]] += 1
            else:
                dict_of_words[words[1]] = 1
    return dict_of_words


def create_num_of_word_occurrences(word):
    dict_of_occurrences = count_tail_occurrences(trigram_tuple, word)
    return dict(sorted(dict_of_occurrences.items(), key=lambda item: item[1], reverse=True))


def return_next_word(word):
    list_of_next_words = list(create_num_of_word_occurrences(word).keys())[:3]
    return random.choice(list_of_next_words)


def verify_sentence_beginning(first_token):
    return first_token[0][0].isupper() \
           and first_token[0][-1] not in '.!?' \
           and first_token[1][-1] not in '.!?'


def return_last_word(sentence):
    return sentence.split(' ')[-1]


def get_sentence_beginning(trigram_list):
    first_tuple = random.choice(trigram_list)
    while True:
        if verify_sentence_beginning(first_tuple[0].split()):
            break
        else:
            first_tuple = random.choice(trigram_list)
    return first_tuple


def add_words_to_sentence(sentence, two_words):
    two_words = return_last_word(sentence) + ' ' + return_next_word(two_words)
    sentence = f' {two_words.split()[1]}'
    return two_words, sentence


def generate_pseudo_sentence(trigram_list):
    first_tuple = get_sentence_beginning(trigram_list)
    first_two_words = first_tuple[0]
    pseudo_sentence = first_two_words
    last_word = return_last_word(pseudo_sentence)
    next_two_words = last_word + ' ' + return_next_word(pseudo_sentence)
    next_word = next_two_words.split()[1]
    pseudo_sentence += f' {next_word}'
    while len(pseudo_sentence.split()) < 5:
        next_two_words, sentence_part = add_words_to_sentence(pseudo_sentence, next_two_words)
        pseudo_sentence += sentence_part
    while next_two_words[-1] not in '.?!':
        next_two_words, sentence_part = add_words_to_sentence(pseudo_sentence, next_two_words)
        pseudo_sentence += sentence_part
    print(pseudo_sentence)


if __name__ == "__main__":
    f = open_file()
    trigram_tuple = create_trigrams(f)
    first_tuple = random.choice(trigram_tuple)

    for i in range(10):
        generate_pseudo_sentence(trigram_tuple)
