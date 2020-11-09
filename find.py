import sys
import regex as re
from collections import Counter
import multiprocessing
from functools import partial


def get_soundex_code(word):

    # Characters that needs to be removed
    characters_to_remove = "aeiouy"

    # Characters that needs to be replaced and creating letters mapping table
    to_replace = {'1': ['b', 'f', 'p', 'v'],
                  '2': ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z'],
                  '3': ['d', 't'],
                  '4': ['l'],
                  '5': ['m', 'n'],
                  '6': ['r']}

    mapping_table = {}

    for value, group in to_replace.items():
        for char in group:
            mapping_table[char] = value

    # Gets first letter
    first_letter = word[0].lower()

    # Characters h and w removed
    code = first_letter + re.sub(r'[hw]*', '', word[1:])

    # Replaces letters with numbers assigned to those letters and joins string
    code = "".join([mapping_table.get(char, char) for char in code])

    # Removes adjacent numbers
    code = re.sub(r'([1-6])\1+', r'\1', code)

    # Removing not needed characters
    code = first_letter + \
        re.sub("[" + characters_to_remove + "]", "", code[1:])

    # If first letter is number it chages it to first letter of word
    code = re.sub(r'[1-6]', first_letter, code[0]) + code[1:]

    # Returns word soundex code, if code is shorter than 3 digists it adds 0
    return code[:4].ljust(4, "0").upper()


def get_word(word, input_word):

    # Returns similar requested word by Soundex algorithm, and cleans returned word from unwanted symbols
    if get_soundex_code(input_word) == get_soundex_code(word):
        word = re.sub(r'[^a-zA-Z ]+', '', word)
        return word


if __name__ == "__main__":

    # Adding arguments to CLI, script, requsting text document, requesting a word for search. Also handling user input errors.
    script = sys.argv[0]

    try:
        filename = sys.argv[1]
    except IndexError:
        print("Please specify text file name as second argument")
        sys.exit()

    try:
        requested_word = sys.argv[2]
    except:
        print("Please specify a word as third argument")
        sys.exit()

    if not (re.match('^[a-zA-Z]+$', requested_word)):
        print("Input word must contain only letters no special symbols or numbers")
        sys.exit()

    # Putting all words from txt file to list
    list_of_words = open(filename, encoding="utf8",
                         buffering=20000000).read().split()

    # Adding some Concurrency
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as p:
        results = p.map(
            partial(get_word, input_word=requested_word), list_of_words)
        p.close()
        p.join()

    # Counts how many times same word appears in  list
    counter = Counter(results)
    del counter[None]

    # Sorts list by count number
    top = sorted(counter, key=counter.get, reverse=True)[:5]

    # Prints top similar words
    for place in top:
        print(place)
