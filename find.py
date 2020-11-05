import sys
import regex as re
from collections import Counter
import multiprocessing
from functools import partial


def get_soundex_code(word):

    # Gets first letter
    first_letter = word[0]

    # Characters that needs to be removes
    characters_to_remove = "aeiouyhw"

    # Removes not needed characters
    new_word = first_letter + \
        re.sub("[" + characters_to_remove + "]", "", word[1:])

    to_replace = {('b', 'f', 'p', 'v'): "1", ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): "2", ('d', 't'): "3", ('l'): "4", ('m', 'n'): "5", ('r'): "6"}
    code = []

    # Replaces letters with numbers assigned to those letters
    for char in new_word:
        for group, value in to_replace.items():
            if char in group:
                code.append(value)
            else:
                code.append(value)

    # Joins list as string
    code = "".join(code)

    # Removes adjacent letters
    code = re.sub(r'([1-6])\1+', r'\1', code)

    # If first letter is number, converts to word's first letter
    code = re.sub(r'[1-6]', first_letter.upper(), code[0]) + code[1:]

    # Returns word soundex code, if code is shorter than 3 digists it adds 0
    return code[:4].ljust(4, "0")


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

    if set('[~!@#$%^&*()_+{}":;\']+-$0123456789').intersection(requested_word):
    	print("Input word must contain only letters no special symbols")
    	sys.exit()
    	
    # Putting all words from txt file to list
    list_of_words = open(filename, encoding="utf8", buffering=20000000).read().split()

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
