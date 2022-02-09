import mr_count_words
import unittest
import logging
import pytest
import pprint
from CreateLargeText import create_source_words, create_random_files


RANDOM_FILE_SIZE_SMALL = 1000
RANDOM_FILE_SIZE_LARGE = 1000000
RANDOM_FILE_SIZE_VERYLARGE = 100000000

SOURCE_WORDS_SIZE_TINY = 10
SOURCE_WORDS_SIZE_SMALL = 100
SOURCE_WORDS_SIZE_LARGE = 1000
SOURCE_WORDS_SIZE_VERYLARGE = 10000

SMALL_FILE_NAME = "smalltest.txt"
MED_FILE_NAME = "medtest.txt"
LARGE_FILE_NAME = "largetest.txt"

SIMPLE_TEST_FILE_1 = ["simple_test1.txt"]
SIMPLE_TEST_RESULTS_1 = [('hello', 1), ('world', 1)]
SIMPLE_TEST_FILE_2 = ["simple_test2.txt"]
SIMPLE_TEST_RESULTS_2 = [('lorem', 40), ('ipsum', 29)]
SIMPLE_TEST_FILE_3 = ["simple_test3.txt"]
SIMPLE_TEST_RESULTS_3 = [('lorem', 1),
                         ('ipsum', 1),
                         ('dolor', 1),
                         ('sit', 1),
                         ('amet', 1),
                         ('consectetur', 1),
                         ('adipiscing', 1),
                         ('elit', 1),
                         ('etiam', 1),
                         ('tempus', 1),
                         ('viverra', 1),
                         ('nisi', 1),
                         ('id', 1)]

EDGE_TEST_FILE_BLANK = ["edge_test_blank.txt"]
EDGE_TEST_RESULTS_BLANK = []
EDGE_TEST_FILE_PUNCTUATION = ["edge_test_punctuation.txt"]
EDGE_TEST_RESULTS_PUNCTUATION = []
EDGE_TEST_FILE_LONG_WORD = ["edge_test_long_word.txt"]
EDGE_TEST_RESULTS_LONG_WORD = [
    ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 1)]


class TestMapReduce(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(filename='test_count_words.log',
                            encoding='utf-8', level=logging.DEBUG)

    def test_simple_files(self):
        '''  Tests 3 different simple files with low word counts
        File1: hello world
        File2: repeating lorem ipsum
        File3: longer lorem ipsum paragraph
        File4: all 3 files together
        '''
        logging.info('Starting tests for word_count')
        word_counts, count_time = mr_count_words.main(SIMPLE_TEST_FILE_1)
        logging.debug(
            f'In test_simple_files, count_time: {count_time} - tested file 1: {SIMPLE_TEST_FILE_1}. Counts from mr_count_words: {word_counts}, desired result: {SIMPLE_TEST_RESULTS_1}')
        self.assertEqual(word_counts, SIMPLE_TEST_RESULTS_1)

        word_counts, count_time = mr_count_words.main(SIMPLE_TEST_FILE_2)
        logging.debug(
            f'In test_simple_files, count_time: {count_time} - tested file 2: {SIMPLE_TEST_FILE_2}. Counts from mr_count_words: {word_counts}, desired result: {SIMPLE_TEST_RESULTS_2}')
        self.assertEqual(word_counts, SIMPLE_TEST_RESULTS_2)

        word_counts, count_time = mr_count_words.main(SIMPLE_TEST_FILE_3)
        logging.debug(
            f'In test_simple_files, count_time: {count_time} - tested file 3: {SIMPLE_TEST_FILE_3}. Counts from mr_count_words: {word_counts}, desired result: {SIMPLE_TEST_RESULTS_3}')
        self.assertEqual(word_counts, SIMPLE_TEST_RESULTS_3)

        word_counts, count_time = mr_count_words.main(
            SIMPLE_TEST_FILE_1 + SIMPLE_TEST_FILE_2 + SIMPLE_TEST_FILE_3)
        logging.debug(
            f'In test_simple_files, count_time: {count_time} - tested file 1, 2, 3: {SIMPLE_TEST_FILE_1} and {SIMPLE_TEST_FILE_2} and {SIMPLE_TEST_FILE_3}. Counts from mr_count_words: {word_counts}, desired result: {SIMPLE_TEST_RESULTS_1 + SIMPLE_TEST_RESULTS_2 + SIMPLE_TEST_RESULTS_3}')
        self.assertEqual(word_counts, [('lorem', 41), ('ipsum', 30), ('hello', 1), ('world', 1), ('dolor', 1), ('sit', 1), ('amet', 1), (
            'consectetur', 1), ('adipiscing', 1), ('elit', 1), ('etiam', 1), ('tempus', 1), ('viverra', 1), ('nisi', 1), ('id', 1)])

    def test_edge_case_files(self):
        '''  Tests 3 different edge case files that should have no word output or 1 word
        File1: blank file
        File2: file with puctuation
        File3: one long word
        File4: all 3 files together
        '''
        word_counts, count_time = mr_count_words.main(EDGE_TEST_FILE_BLANK)
        logging.debug(
            f'In test_edge_case_files, count_time: {count_time} - tested blank case: {EDGE_TEST_FILE_BLANK}. Counts from mr_count_words: {word_counts}, desired result: {EDGE_TEST_RESULTS_BLANK}')
        self.assertEqual(word_counts, EDGE_TEST_RESULTS_BLANK)

        word_counts, count_time = mr_count_words.main(
            EDGE_TEST_FILE_PUNCTUATION)
        logging.debug(
            f'In test_edge_case_files, count_time: {count_time} - tested punctuation case: {EDGE_TEST_FILE_PUNCTUATION}. Counts from mr_count_words: {word_counts}, desired result: {EDGE_TEST_RESULTS_PUNCTUATION}')
        self.assertEqual(word_counts, EDGE_TEST_RESULTS_PUNCTUATION)

        word_counts, count_time = mr_count_words.main(EDGE_TEST_FILE_LONG_WORD)
        logging.debug(
            f'In test_edge_case_files, count_time: {count_time} - tested long word case: {EDGE_TEST_FILE_LONG_WORD}. Counts from mr_count_words: {word_counts}, desired result: {EDGE_TEST_RESULTS_LONG_WORD}')
        self.assertEqual(word_counts, EDGE_TEST_RESULTS_LONG_WORD)

        word_counts, count_time = mr_count_words.main(
            EDGE_TEST_FILE_BLANK + EDGE_TEST_FILE_PUNCTUATION + EDGE_TEST_FILE_LONG_WORD)
        logging.debug(
            f'In test_edge_case_files, count_time: {count_time} - tested edge cases together: {EDGE_TEST_FILE_BLANK}, {EDGE_TEST_FILE_PUNCTUATION}, {EDGE_TEST_FILE_LONG_WORD}. Counts from count_words: {word_counts}, desired result: {[]}')
        self.assertEqual(word_counts, EDGE_TEST_RESULTS_LONG_WORD)

    def test_map_find_words(self):
        '''  Tests the map_find_words function with simple test case files'''
        FIND_WORDS_RESULTS_1 = [['hello', 1], ['world', 1]]
        FIND_WORDS_RESULTS_2 = [['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['lorem', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1], ['ipsum', 1]]
        FIND_WORDS_RESULTS_3 = [['lorem', 1], ['ipsum', 1], ['dolor', 1], ['sit', 1], ['amet', 1], ['consectetur', 1], [
            'adipiscing', 1], ['elit', 1], ['etiam', 1], ['tempus', 1], ['viverra', 1], ['nisi', 1], ['id', 1]]

        word_counts = mr_count_words.map_find_words(SIMPLE_TEST_FILE_1[0])
        logging.debug(
            f'In test_map_find_words - tested find words: {SIMPLE_TEST_FILE_1[0]}. Counts from map_find_words: {word_counts}, desired result: {FIND_WORDS_RESULTS_1}')
        self.assertEqual(word_counts, FIND_WORDS_RESULTS_1)

        word_counts = mr_count_words.map_find_words(SIMPLE_TEST_FILE_2[0])
        logging.debug(
            f'In test_map_find_words - tested find words: {SIMPLE_TEST_FILE_2[0]}. Counts from map_find_words: {word_counts}, desired result: {FIND_WORDS_RESULTS_2}')
        self.assertEqual(word_counts, FIND_WORDS_RESULTS_2)

        word_counts = mr_count_words.map_find_words(SIMPLE_TEST_FILE_3[0])
        logging.debug(
            f'In test_map_find_words - tested find words: {SIMPLE_TEST_FILE_3[0]}. Counts from map_find_words: {word_counts}, desired result: {FIND_WORDS_RESULTS_3}')
        self.assertEqual(word_counts, FIND_WORDS_RESULTS_3)

    def test_reduce_count_words(self):
        '''  Tests the reduce_count_words function with simple input'''
        FIND_WORDS_INPUT_1 = ('hello', [1])
        FIND_WORDS_INPUT_2 = ('lorem', [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        FIND_WORDS_INPUT_3 = ('dolor', [1, 1, 1, 1, 1, 1, 1, 1])

        FIND_WORDS_RESULTS_1 = ('hello', 1)
        FIND_WORDS_RESULTS_2 = ('lorem', 40)
        FIND_WORDS_RESULTS_3 = ('dolor', 8)

        word_counts = mr_count_words.reduce_count_words(FIND_WORDS_INPUT_1)
        logging.debug(
            f'In test_reduce_count_words - tested reduce count: {FIND_WORDS_INPUT_1}. Counts from reduce_count_words: {word_counts}, desired result: {FIND_WORDS_RESULTS_1}')
        self.assertEqual(word_counts, FIND_WORDS_RESULTS_1)

        word_counts = mr_count_words.reduce_count_words(FIND_WORDS_INPUT_2)
        logging.debug(
            f'In test_reduce_count_words - tested reduce count: {FIND_WORDS_INPUT_2}. Counts from reduce_count_words: {word_counts}, desired result: {FIND_WORDS_RESULTS_2}')
        self.assertEqual(word_counts, FIND_WORDS_RESULTS_2)

        word_counts = mr_count_words.reduce_count_words(FIND_WORDS_INPUT_3)
        logging.debug(
            f'In test_reduce_count_words - tested reduce count: {FIND_WORDS_INPUT_3}. Counts from reduce_count_words: {word_counts}, desired result: {FIND_WORDS_RESULTS_3}')
        self.assertEqual(word_counts, FIND_WORDS_RESULTS_3)

    def test_random_files(self):
        ''' Uses the CreateLargeText.py to create random text files and tests the mr_count_words function against this '''

        source_words = create_source_words(SOURCE_WORDS_SIZE_SMALL)
        created_file_size, created_word_counts, created_word_count_list, created_file_names = create_random_files(
            SMALL_FILE_NAME, RANDOM_FILE_SIZE_SMALL, source_words, num_files=10)
        counted_word_counts, total_time = mr_count_words.main(
            created_file_names)
        logging.debug(
            f'In test_random_files, total_time: {total_time} - tested random files: {created_file_names}. Counts from mr_count_words: {counted_word_counts}, desired result: {created_word_counts}')
        self.assertEqual(created_word_counts, counted_word_counts)

        source_words = create_source_words(SOURCE_WORDS_SIZE_LARGE)
        created_file_size, created_word_counts, created_word_count_list, created_file_names = create_random_files(
            MED_FILE_NAME, RANDOM_FILE_SIZE_LARGE, source_words, num_files=10)
        counted_word_counts, total_time = mr_count_words.main(
            created_file_names)
        logging.debug(
            f'In test_random_files, total_time: {total_time} - tested random files: {created_file_names}. Counts from mr_count_words: {counted_word_counts}, desired result: {created_word_counts}')
        self.assertEqual(created_word_counts, counted_word_counts)

        source_words = create_source_words(SOURCE_WORDS_SIZE_VERYLARGE)
        created_file_size, created_word_counts, created_word_count_list, created_file_names = create_random_files(
            LARGE_FILE_NAME, RANDOM_FILE_SIZE_VERYLARGE, source_words, num_files=10)
        counted_word_counts, total_time = mr_count_words.main(
            created_file_names)
        logging.debug(
            f'In test_random_files, total_time: {total_time} - tested random files: {created_file_names}. Counts from mr_count_words: {counted_word_counts}, desired result: {created_word_counts}')
        self.assertEqual(created_word_counts, counted_word_counts)


if __name__ == '__main__':
    unittest.main()
