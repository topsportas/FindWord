import sys
import regex as re

def get_soundex_code(word):

	# Gets first letter
	first_letter = word[0]

	# Characters that needs to be removes
	characters_to_remove = "aeiouyhw"

	# Removes not needed characters
	new_word = first_letter + re.sub("[" + characters_to_remove + "]", "", word[1:])

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


if __name__ == "__main__":

    script = sys.argv[0]
    filename = sys.argv[1]
    requested_word = sys.argv[2]
    list_of_words = open(filename, encoding="utf8").read().split()
    for word in list_of_words:
        if get_soundex_code(requested_word) == get_soundex_code(word):
            print(word)
