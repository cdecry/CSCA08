"""CSC108/A08: Fall 2021 -- Assignment 3: arxiv.org

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Anya Tafliovich.

"""

import copy  # needed in examples of functions that modify input dict
from typing import Dict, List, TextIO

# remove unused constants from this import statement when you are
# finished your assignment
from constants import (ID, TITLE, CREATED, MODIFIED, AUTHORS,
                       ABSTRACT, END, SEPARATOR, NameType,
                       ArticleType, ArxivType)


EXAMPLE_ARXIV = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '031': {
        'identifier': '031',
        'title': 'Calculus is the best course ever',
        'created': None,
        'modified': '2021-09-02',
        'authors': [('Breuss', 'Nataliya')],
        'abstract': '''We discuss the reasons why Calculus I
is the best course.'''},
    '067': {'identifier': '067',
            'title': 'Discrete Mathematics is the best course ever',
            'created': '2021-09-02',
            'modified': '2021-10-01',
            'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
            'abstract': ('We explain why Discrete Mathematics is the best ' +
                         'course of all times.')},
    '827': {
        'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')],
        'abstract': '''We show a formal proof that the University of
Toronto is the best university.'''},
    '042': {
        'identifier': '042',
        'title': None,
        'created': '2021-05-04',
        'modified': '2021-05-05',
        'authors': [],
        'abstract': '''This is a very strange article with no title
and no authors.'''}
}

EXAMPLE_BY_AUTHOR = {
    ('Ponce', 'Marcelo'): ['008', '827'],
    ('Tafliovich', 'Anya Y.'): ['008', '827'],
    ('Bretscher', 'Anna'): ['067', '827'],
    ('Breuss', 'Nataliya'): ['031'],
    ('Pancer', 'Richard'): ['067']
}


# We provide this PARTIAL docstring to show the use of examples.
def make_author_to_articles(id_to_article: ArxivType) -> Dict[NameType,
                                                              List[str]]:
    """Return a new dict that maps each author name to a list in lexigraphic
    order of the IDs of articles from written by that author, from
    id_to_article.

    >>> make_author_to_articles(EXAMPLE_ARXIV) == EXAMPLE_BY_AUTHOR
    True
    >>> EX_ARXIV = {
    ... '00AAS.8D': {
    ... 'identifier': '008',
    ... 'title': 'Intro to CS is the best course ever',
    ... 'created': '2021-09-01',
    ... 'modified': None,
    ... 'authors': [],
    ... 'abstract': '''We present clear evidence that Introduction to
    ...                Computer Science is the best course.'''}}
    >>> make_author_to_articles(EX_ARXIV) == {}
    True
    >>> EX_ARXIV2 = {
    ... '00AAS.8D': {
    ... 'identifier': '00AAS.8D',
    ... 'title': None,
    ... 'created': '2021-09-01',
    ... 'modified': None,
    ... 'authors': [('Smith', 'John')],
    ... 'abstract': '''xyz'''}}
    >>> make_author_to_articles(EX_ARXIV2)
    {('Smith', 'John'): ['00AAS.8D']}
    """

    author_to_article = {}

    for article in id_to_article:
        for author in id_to_article[article][AUTHORS]:
            if author not in author_to_article:
                author_to_article[author] = [article]
            else:
                author_to_article[author].append(article)

    for author in author_to_article:
        author_to_article[author].sort()

    return author_to_article

def get_coauthors(id_to_article: ArxivType, author: NameType) -> List[NameType]:

    """Return a list of coauthors of the given author, author, from articles
    in id_to_article, sorted in lexicographic order.

    >>> get_coauthors(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.'))
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo')]
    >>> get_coauthors(EXAMPLE_ARXIV, ('Apple', 'Banana'))
    []
    >>> get_coauthors(EXAMPLE_ARXIV, ('Bruess', 'Nataliya'))
    []
    >>> get_coauthors(EXAMPLE_ARXIV, ('Ponce', 'Marcelo'))
    [('Bretscher', 'Anna'), ('Tafliovich', 'Anya Y.')]
    >>> EX_ARXIV = {
    ... '00AAS.8D': {
    ... 'identifier': '00AAS.8D',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [('bob', 'smith'), ('bob', 'smith'), ('john', 'doe')],
    ... 'abstract': None},
    ... 'abdcd': {
    ... 'identifier': 'abdcd',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [('bob', 'smith'), ('john', 'doe')],
    ... 'abstract': None}}
    >>> get_coauthors(EX_ARXIV, ('john', 'doe'))
    [('bob', 'smith')]
    """

    unfiltered_coauthors = []
    coauthors = []
    author_to_articles = make_author_to_articles(id_to_article)

    if author in author_to_articles:
        for article in author_to_articles[author]:
            for coauthor in id_to_article[article][AUTHORS]:
                unfiltered_coauthors.append(coauthor)
        for coauthor in unfiltered_coauthors:
            if coauthor not in coauthors and coauthor != author:
                coauthors.append(coauthor)
        coauthors.sort()
    return coauthors

def get_most_published_authors(id_to_article: ArxivType) -> List[NameType]:

    """Return a list of the author of dictionary of articles id_to_authors who
    has published the most articles. If there is a tie, return the list of
    authors tied, in lexicographic order.

    >>> get_most_published_authors(EXAMPLE_ARXIV)
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    >>> EX_ARXIV = {
    ... '00AAS.8D': {
    ... 'identifier': '00AAS.8D',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [],
    ... 'abstract': None}}
    >>> get_most_published_authors(EX_ARXIV)
    []
    >>> EX_ARXIV2 = {
    ... '00AAS.8D': {
    ... 'identifier': '00AAS.8D',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [('mouse', 'pad'), ('kEy', 'board')],
    ... 'abstract': None},
    ... 'abdcd': {
    ... 'identifier': 'abdcd',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [('kEy', 'board')],
    ... 'abstract': None}}
    >>> get_most_published_authors(EX_ARXIV2)
    [('kEy', 'board')]
    """

    most_published = []
    num_articles_to_author = {}
    highest = 0
    author_to_articles = make_author_to_articles(id_to_article)

    for author in author_to_articles:
        num_articles = len(author_to_articles[author])
        if num_articles > highest:
            highest = num_articles
        if num_articles not in num_articles_to_author:
            num_articles_to_author[num_articles] = [author]
        else:
            num_articles_to_author[num_articles].append(author)
    if highest in num_articles_to_author:
        most_published.extend(num_articles_to_author[highest])
    most_published.sort()
    return most_published

def suggest_collaborators(id_to_article: ArxivType,
                          author: NameType) -> List[NameType]:

    """Return a lexicographic-sorted list of suggested authors for the author,
    author, to colloborate with.

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Pancer', 'Richard'))
    [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.'))
    [('Pancer', 'Richard')]
    >>> EX_ARXIV = {
    ... '00AAS.8D': {
    ... 'identifier': '00AAS.8D',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [],
    ... 'abstract': None}}
    >>> suggest_collaborators(EXAMPLE_ARXIV, ('dog', 'cat'))
    []
    >>> EX_ARXIV = {
    ... '00AAS.8D': {
    ... 'identifier': '00AAS.8D',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [('mouse', 'pad'), ('kEy', 'board')],
    ... 'abstract': None},
    ... 'abdcd': {
    ... 'identifier': 'abdcd',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [('kEy', 'board')],
    ... 'abstract': None}}
    >>> suggest_collaborators(EX_ARXIV, ('mouse', 'pad'))
    []
    >>> EX_ARXIV2 = {
    ... '00AAS.8D': {
    ... 'identifier': '00AAS.8D',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [('x', 'a'), ('a', 'a')],
    ... 'abstract': None},
    ... 'abdcd': {
    ... 'identifier': 'abdcd',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [('x', 'a'), ('a', 'z'), ('y', 'z')],
    ... 'abstract': None},
    ... 'third': {
    ... 'identifier': 'abdcd',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [('x', 'a'), ('b', 'd'), ('b', 'c')],
    ... 'abstract': None}}
    >>> suggest_collaborators(EX_ARXIV2, ('a', 'a'))
    [('a', 'z'), ('b', 'c'), ('b', 'd'), ('y', 'z')]
    """

    suggested = []
    coauthors = get_coauthors(id_to_article, author)

    for coauthor in coauthors:
        for other in get_coauthors(id_to_article, coauthor):
            if (other not in coauthors and other not in suggested and
                    other != author):
                suggested.append(other)

    return suggested

def has_prolific_authors(author_to_articles: Dict[NameType, List[str]],
                         article: ArticleType, min_publications: int) -> bool:

    """Return True if and only if article, article has at least one author from
    author_to_articles that has more than the minimum amount of articicles to be
    considered prolific, min_publications.

    Preconditions: min_publications >= 0

    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV['008'], 2)
    True
    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV['031'], 2)
    False
    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV['008'], 0)
    True
    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV['008'], 100)
    False
    >>> EXAMPLE_BY_AUTHOR2 = {}
    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR2, EXAMPLE_ARXIV['008'], 2)
    False
    >>> EX_ARXIV = {
    ... '00AAS.8D': {
    ... 'identifier': '00AAS.8D',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [],
    ... 'abstract': None},
    ... 'abdcd': {
    ... 'identifier': 'abdcd',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [],
    ... 'abstract': None},
    ... 'third': {
    ... 'identifier': 'abdcd',
    ... 'title': None,
    ... 'created': None,
    ... 'modified': None,
    ... 'authors': [],
    ... 'abstract': None}}
    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EX_ARXIV['00AAS.8D'], 0)
    False
    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR2, EX_ARXIV['00AAS.8D'], 0)
    False
    """

    author_to_num_articles = {}

    for author in author_to_articles:
        author_to_num_articles[author] = len(author_to_articles[author])
    for author in article[AUTHORS]:
        if author in author_to_num_articles:
            if author_to_num_articles[author] >= min_publications:
                return True
    return False

# We provide this PARTIAL docstring to show use of copy.deepcopy.
def keep_prolific_authors(id_to_article: ArxivType,
                          min_publications: int) -> None:
    """Modify id_to_article so that it contains only articles published by
    at least one author with min_publications or more articles published.

    Preconditions: min_publications >= 0

    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 2)
    >>> len(arxiv_copy)
    3
    >>> '008' in arxiv_copy and '067' in arxiv_copy and '827' in arxiv_copy
    True
    """

    author_to_articles = make_author_to_articles(id_to_article)

    for article in id_to_article.copy():
        if not has_prolific_authors(author_to_articles,
                                    id_to_article.copy()[article],
                                    min_publications):
            id_to_article.pop(article)

# Note that we do not include example calls since the function works
# on an input file.
def read_arxiv_file(afile: TextIO) -> ArxivType:
    """Return a dict containing all arxiv information in afile.

    Precondition: afile is open for reading
                  afile is in the format described in the handout
    """

    id_to_article = {}
    article = {}
    line = afile.readline()
    while line != '':
        article[ID] = clean(line)
        article[TITLE] = clean(afile.readline())
        article[CREATED] = clean(afile.readline())
        article[MODIFIED] = clean(afile.readline())
        article[AUTHORS] = []
        line = afile.readline()

        while line != '\n':
            name_list = clean(line).split(SEPARATOR)
            name = (name_list[0], name_list[1])
            article[AUTHORS].append(name)
            line = afile.readline()

        article[AUTHORS].sort()
        line = afile.readline()
        abstract_string = ''

        while clean(line) != END:
            abstract_string += line
            line = afile.readline()

        article[ABSTRACT] = clean(abstract_string)
        id_to_article[article[ID]] = article
        article = {}
        line = afile.readline()

    return id_to_article

def clean(line: str) -> str:
    """Return modified version of the string, line without trailing whitespaces
    or new line symbols at the end. Return None if line is blank after being
    modified.

    >>> clean('0.830\\n')
    '0.830'
    >>> clean('This is a \\n test\\n')
    'This is a \\n test'
    >>> clean('@398\\n987\\n')
    '@398\\n987'
    >>> clean('j\\n\\n\\n\\n\\n')
    'j\\n\\n\\n\\n'
    >>> clean('\\n\\nblahblah\\n\\n\\n\\n      \\n')
    '\\n\\nblahblah\\n\\n\\n\\n      '
    """

    line = line[:-1]

    if line == '':
        return None

    return line

if __name__ == '__main__':

    import doctest
    doctest.testmod()

    with open('Assignment3/starter/example_data.txt') as example_data:
        example_arxiv = read_arxiv_file(example_data)
        print('Did we produce a correct dict? ',
              example_arxiv == EXAMPLE_ARXIV)

    # uncomment to work with a larger data set
    with open('Assignment3/starter/data.txt') as data:
        arxiv = read_arxiv_file(data)

    authors_to_articles = make_author_to_articles(arxiv)
    #most_published = get_most_published_authors(arxiv)
    #print(most_published)
    #print(get_coauthors(arxiv, ('Varanasi', 'Mahesh K.')))  # one
    #print(get_coauthors(arxiv, ('Chablat', 'Damien')))  # many
    #print(arxiv)
