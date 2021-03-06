from collections import namedtuple

import matplotlib.pylab as plt
from CaesarCrypt import caesar_decrypt
from CheckTheLanguageOfThePhrase import CheckTheLanguageOfThePhrase

ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERS = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def clean_other_symbols(text_to_clean: str) -> str:
    new_char_to_return: str = ''

    for char in text_to_clean:

        if char.upper() in LETTERS:
            new_char_to_return += char

    return new_char_to_return


def crack_with_brute_force(crypted_message: str) -> list:
    KEY = 1

    options_secret_word: list = []
    key_inside: int = len(ALPHABET)

    for number_inside_key in range(key_inside):

        plain_text: str = ''

        for char in crypted_message:
            index = ALPHABET.find(char)
            index = (index - number_inside_key) % len(ALPHABET)

            plain_text += ALPHABET[index]

        options_secret_word.append(plain_text)

    return options_secret_word


def _return_frequency_dictionary_of_a_phrase(text_to_analyse: str) -> {}:
    text_to_analyse = text_to_analyse.upper()

    letter_frequencies = {}

    for letter in LETTERS:
        letter_frequencies[letter] = 0

    for letter in text_to_analyse:
        if letter in LETTERS:
            letter_frequencies[letter] += 1

    return letter_frequencies


def plot_distribution(frequencies: {}) -> None:
    plt.bar(frequencies.keys(), frequencies.values())
    plt.show()


def _calculate_key(char_to_check: str) -> list:
    most_famous_letters = ['E', 'A', 'R', 'I']
    possible_keys = []

    for letter in most_famous_letters:

        difference = LETTERS.find(char_to_check) - LETTERS.find(letter)
        if difference > 0:
            difference = abs(len(LETTERS) - difference)

            possible_keys.append(difference)
        elif difference == 0:
            possible_keys.append(LETTERS.find('E'))
        else:
            possible_keys.append(abs(difference))

    return possible_keys


def caesar_crack_with_smart_analysis(text_to_analyse: str) -> []:
    list_of_possibilities = []

    freq = _return_frequency_dictionary_of_a_phrase(text_to_analyse)

    formatted_freq_list = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    char_to_check = formatted_freq_list[0][0]
    position_keys = _calculate_key(char_to_check)

    for index in position_keys:
        message_decrypted = caesar_decrypt(text_to_analyse, index)
        list_of_possibilities.append(message_decrypted)

    return list_of_possibilities


def caesar_crack_with_smart_analysis_and_machine_thinking(text_to_analyse: str) -> tuple:
    list_of_possibilities = []

    freq = _return_frequency_dictionary_of_a_phrase(text_to_analyse)

    formatted_freq_list = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    char_to_check = formatted_freq_list[0][0]
    position_keys = _calculate_key(char_to_check)

    automatic_checker = CheckTheLanguageOfThePhrase()

    info_to_return = namedtuple("info_to_return", ["found", "type_language", "number_of_tentatives",
                                                   "list_of_possibilities"])

    for index in position_keys:
        message_decrypted = caesar_decrypt(text_to_analyse, index)

        automatic_checker.break_the_phrase(message_decrypted)
        found_language = automatic_checker.return_the_language()

        if found_language.found:
            list_of_possibilities.append(message_decrypted)
            return info_to_return(True, found_language.type_language, len(list_of_possibilities), list_of_possibilities)
            break
        list_of_possibilities.append(message_decrypted)

    return info_to_return(False, "None", len(list_of_possibilities), list_of_possibilities)
