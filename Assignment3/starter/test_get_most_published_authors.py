"""CSC108/A08: Fall 2021 -- Assignment 3: arxiv.org

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Anya Tafliovich.

"""

import copy
import unittest
from arxiv_functions import get_most_published_authors as get_mpas
from arxiv_functions import EXAMPLE_ARXIV


class TestGetMostPublishedAuthors(unittest.TestCase):
    """Test the function get_most_published_authors."""

    def test_handout_example(self):
        """Test get_most_published_authors with the handout example.
        """

        arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
        expected = [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_no_authors(self):
        """Test get_most_published_authors when all articles have no authors.
        """

        arxiv_copy = {'00AAS.8D': {
            'identifier': '00AAS.8D',
            'title': None,
            'created': None,
            'modified': None,
            'authors': [],
            'abstract': None}}
        expected = []
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_author_order(self):
        """Test get_most_published_authors when there is a tie between multiple
        authors. (Test for lexicographic order)
        """

        arxiv_copy = {
            'zzz':{
                'identifier': 'zzz',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x', 'a'), ('y', 'z'), ('a', 'a')],
                'abstract': None},
            'aaa': {
                'identifier': 'aaa',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x', 'a'), ('a', 'z'), ('y', 'z'), ('a', 'a')],
                'abstract': None},
            'xx': {
                'identifier': 'xx',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('y', 'z'), ('a', 'a'), ('x', 'a'), ('b', 'd'), ('b', 'c')],
                'abstract': None}}
        expected = [('a', 'a'), ('x', 'a'), ('y', 'z')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_empty_arxiv(self):
        """Test get_most_published_authors with an empty arxiv dict.
        """

        arxiv_copy = {}
        expected = []
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_only_one_author(self):
        """Test get_most_published_authors with an arxiv containg articles
        all published by the same author.
        """

        arxiv_copy = {
            '1':{
                'identifier': '1',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x', 'a')],
                'abstract': None},
            '2': {
                'identifier': '2',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x', 'a')],
                'abstract': None},
            '3': {
                'identifier': '3',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x', 'a')],
                'abstract': None}}
        expected = [('x', 'a')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_single_most_published(self):
        """Test get_most_published_authors where there should only be one
        author who is the most published
        """

        arxiv_copy = {
            '1':{
                'identifier': '1',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x', 'a'), ('a', 'b')],
                'abstract': None},
            '2': {
                'identifier': '2',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x', 'a'), ('g', 'd')],
                'abstract': None},
            '3': {
                'identifier': '3',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x', 'a'), ('a', 'b')],
                'abstract': None}}
        expected = [('x', 'a')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_author_names(self):
        """Test get_most_published_authors where the most published authors
        has different characters in name
        """

        arxiv_copy = {
            '1':{
                'identifier': '1',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x.$(#%', 'a'), ('a. . .', '. . .b')],
                'abstract': None},
            '2': {
                'identifier': '2',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x.$(#%', 'a'), ('g', 'd')],
                'abstract': None},
            '3': {
                'identifier': '3',
                'title': None,
                'created': None,
                'modified': None,
                'authors': [('x.$(#', 'a'), ('a. . .', '. . .b')],
                'abstract': None}}
        expected = [('a. . .', '. . .b'), ('x.$(#%', 'a')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_author_name_in_article_info(self):
        """Test get_most_published_authors with an arxiv containg articles
        with title/abstract that also mention author's name.
        """

        arxiv_copy = {
            '1':{
                'identifier': '1',
                'title': '''john doe; john, doe; doe, john;johndoe; john,doe;
                            doe,john;''',
                'created': None,
                'modified': None,
                'authors': [('doe', 'john'), ('person', 'c')],
                'abstract': None},
            '2': {
                'identifier': '1',
                'title': 'beep',
                'created': None,
                'modified': None,
                'authors': [('bob', 'smith'), ('person', 'c')],
                'abstract': '''bob smith; bob, smith; smith, bob;bobsmith;
                               bob,smith; smith,bob;'''}}
        expected = [('person', 'c')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

def message(test_case: dict, expected: list, actual: object) -> str:
    """Return an error message saying the function call
    get_most_published_authors(test_case) resulted in the value
    actual, when the correct value is expected.

    """

    return ("When we called get_most_published_authors(" + str(test_case) +
            ") we expected " + str(expected) +
            ", but got " + str(actual))


if __name__ == '__main__':
    unittest.main(exit=False)
