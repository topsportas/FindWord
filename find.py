import sys
import fuzzywuzzy


if __name__ == "__main__":
	script = sys.argv[0]
	filename = sys.argv[1]
	word = sys.argv[2]
	list_of_words = []
	for words in open(filename, encoding="utf8").read().split():
		list_of_words.append(words)
	print(list_of_words)