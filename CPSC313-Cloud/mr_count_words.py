""" mr_count_words.py
    Author: Nathan Flack
    Date: 2/1/2022
    Assignment: Map Reduce Count Words
"""

from ast import arguments
import logging
import time
import sys
import pprint
import string
from typing import Counter
import basicMR
import count_words

STOP_WORDS = ['a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if',
              'in', 'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the', 'to', 'with']

logging.basicConfig(filename='count_words.log',
                    encoding='utf-8', level=logging.DEBUG)


def map_find_words(file_name):
    """ take a file and return a list of lists where each sublist is a list with the word
    and the number 1 for that file. 
    This may look like: [['foo', 1], ['bar', 1], ['foo', 1], ...]
    """
    logging.info("find_words started")
    logging.info("%s opened", file_name)
    with open(file_name, 'r') as file_object:
        word_list = []
        for line in file_object:
            line = line.translate(str.maketrans('', '', string.punctuation))
            line = line.lower()
            for word in line.split():
                if word.isalpha() and word not in STOP_WORDS:
                    word_list.append([word, 1])
                else:
                    logging.warning(
                        f'Have either a non-alphabetic word or a stop-word. Word is {word}')
    logging.info("%s closed", file_name)
    logging.info("find_words ended")
    print(word_list)
    return word_list


def reduce_count_words(item):
    """Take an item that is a list, get its word and count and return
    a tuple that is the word with it's summed count. 

    The input may look like [['word1', 1, 1, 1, 1, 1], ['word2', 1, 1, 1]] if it has been partitioned
    Returns the tuple with the word and the summed count
    """
    #logging.info('Count Words Input: ' + pprint.pformat(item))
    return (item[0], sum(item[1]))


def main(*args):
    """ main function: get the files from input or *args Iterate through the files counting 
    words in each file, then combine results from each 

    inside this main function you'll start a timer using time.perf_counter 
    (you'll import the time library), create the SimpleMapReduct class with the 
    find_words and count_words functions, call the objects __call__ method with the input 
    files and a chunksize, sort the list by count in reverse order (highest count first), 
    end the timer with another call to time.perf_counter(), calculate the time spent 
    and you have the map_reduce

    You should also call your previous implementation with the timer calls and then 
    you can compare the time taken to do a set of rather large files (> 1GB) using 
    both approaches. 

    the input will either be system arguements if entered into a console
    or a list object of file name strings if called from a file.
    
    """

    logging.info('----------------------')
    logging.info('Main program started')
    if len(args) == 0:
        file_name_list = sys.argv[1:]
    else:
        file_name_list = args[0]

    map_reduce = basicMR.SimpleMapReduce(map_find_words, reduce_count_words)

    time_start = time.perf_counter()
    final_results = sorted(map_reduce(file_name_list),
                           key=lambda word: word[1], reverse=True)
    time_end = time.perf_counter()
    #logging.debug(
     #    f'\nAfter counting words in all files. \nTotal time taken: {time_end - time_start}  \nTotal number of words: {len(final_results)}. \nWord counts are: \n{pprint.pformat(final_results)}\n')

    logging.info('Main program ended')
    return final_results, time_end - time_start


if __name__ == '__main__':
    main()
