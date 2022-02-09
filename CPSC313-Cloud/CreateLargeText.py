from itertools import count
import string
import requests
from random import randint

CORPUS_COUNT = 10
STOP_WORDS = set([
            'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in', 
            'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the', 'to', 'with',
            ])

def file_to_words(filename):
    """Read a file and return a sequence of (word, occurances) values.
    """
#    TR = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

#    print (multiprocessing.current_process().name, 'reading', filename)
    unique_words = []

    with open(filename, 'rt') as current_file:
        for line in current_file:
            line = line.translate(line.maketrans(string.punctuation, ' ' * len(string.punctuation))) # Strip punctuation
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in unique_words:
                    unique_words.append(word)
    return unique_words

def create_random_files(filename, size, source_words, num_files=1):
    """
    Will create a file of given size (parameter) with name filename (parameter) from source words (parameter)
    Will also split the file into multiple files (mostly for testing merge counts)
        For each file created if split, append the number of the file at the end of filename
        Most of the code is for splitting files. create a list of filenames and derive the file size per split file
    Iterate through the list of filenames (if num_files is 1 then it's the single filename passed)
        Simply get a random word from source words and add it to the file (with a space separator) until you reach file size
        create a word_counts dictionary and add it to a list of all word_counts and to a master word count dictionary
    """
    new_file_names = []
    if num_files > 1:
        for loop_control in range(1, num_files+1):
            new_file_names.append(filename + str(loop_control))
        file_size = size // num_files
    else:
        new_file_names = [filename]
        file_size = size
    master_word_counts = {}
    word_counts_list = []
    master_file_size = 0
    source_length = len(source_words)
    for new_file_name in new_file_names:
        with open(new_file_name, 'w') as new_file:
            cur_file_size = 0
            cur_word_counts = {}
            while cur_file_size < file_size:
                random_word = source_words[randint(0, source_length-1)]
                if random_word.isalpha() and random_word not in STOP_WORDS:
                    new_file.write(random_word + ' ')
                    cur_file_size += len(random_word) + 1
                    cur_word_counts[random_word] = cur_word_counts.get(random_word, 0) + 1
                    master_word_counts[random_word] = master_word_counts.get(random_word, 0) + 1
            master_file_size += cur_file_size
            word_counts_list.append(cur_word_counts)
    master_word_counts = sorted(list(master_word_counts.items()), key=lambda word: word[1], reverse=True)
    return master_file_size, master_word_counts, word_counts_list, new_file_names
     
def create_source_words(count_words):
    # Call a simple dictionary service (found by searching) to get the random word list
    resp = requests.get(f"https://random-word-api.herokuapp.com/word?number={count_words}")
    return list(resp.json())
    
def main():
    while True:
        file_name = input('Enter the desired file name <return to quit>: ')
        if len(file_name) == 0:
            break
        elif file_name.find('.txt') == -1:
            file_name += '.txt'
        desired_size = int(input('Enter the desired file size (in bytes): '))

        random_words = create_source_words(CORPUS_COUNT)

        print(random_words)
        for word in random_words:
            print(f'random word is {word}')

        # Create the new file of random words given the info we have by calling the function
        file_size, word_counts = create_random_files(file_name, desired_size, random_words)    
        print(f'\nA new file named {file_name} was created with size = {file_size}\n')
        print(f'Word counts are: \n{str(word_counts)}')

if __name__== "__main__":
    main()