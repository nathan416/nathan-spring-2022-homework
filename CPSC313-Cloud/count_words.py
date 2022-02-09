from ast import arguments
import logging
import time
import sys
import pprint
import string

STOP_WORDS = ['a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if',
              'in', 'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the', 'to', 'with', '']
time_start = time.time()



def count_words(file_name):
    """take a file and output the word list with the counts for that file as a dictionary. This may look like: [['foo', 22], ['bar', 13], ...]

    Args:
        file_name (str): name of the file to be counted

    Returns:
        dictionary: dictionary of words with their respective counts in value
    """
    with open(file_name, 'r') as file_object:
        time_file = time.time()
        logging.info('[%s][%s seconds since start] %s opened', time.ctime(), time.time() - time_start, file_name)
        file_data = file_object.read()
        file_data = file_data.replace('\n', ' ')
        file_data = file_data.translate(str.maketrans('', '', string.punctuation))
        file_data = file_data.lower()
        string_list = file_data.split(' ')
        results = {}
        for word in string_list:
            include = True
            for k_iterator in STOP_WORDS:
                if k_iterator == word:
                    include = False
            if include and word.isalpha():
                if word not in results:
                    results[word] = 1
                else:
                    results[word] = results[word] + 1
    logging.info('[%s][%s seconds since start] %s closed', time.ctime(), time.time() - time_start, file_name)
    logging.info('[%s][%s seconds since start] %s took %s seconds to complete', time.ctime(), time.time() - time_start, file_name, time.time() - time_file)
    return results


def combine_word_counts(file_name_list):
    """Iterate through the files counting words in each file, then combine results from each

    Args:
        file_name_list (list): [iterable of file]

    Returns:
        [type]: [description]
    """
    final_results = {}
    for file_name in file_name_list:
        count_results = count_words(file_name)
        for word in count_results:
            if word not in final_results:
                final_results[word] = count_results[word]
            else:
                final_results[word] = final_results[word] + count_results[word]
    return final_results


def main(*args):
    """main function: get the files from input (or *args). Iterate through the files counting words in each file, then combine results from each

    Returns:
        [type]: [description]
    """
    logging.basicConfig(filename='count_words.log',
                    encoding='utf-8', level=logging.DEBUG)
    logging.info('----------------------')
    logging.info('[%s][%s seconds since start] Program started', time.ctime(), time.time() - time_start)
    if len(args) == 0:
        file_name_list = sys.argv[1:]
    else:
        file_name_list = args
    final_results = combine_word_counts(file_name_list)
    return final_results

if __name__ == '__main__':
    main()
