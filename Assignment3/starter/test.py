
from doctest import Example
import copy
from typing import Dict, List, Tuple, Union, TextIO

afile = open('/Users/crystal/Desktop/CSCA08/Assignment3/starter/play.txt')

def read_lines(play, character):
    """ (file open for reading, str) -> list of str
    Return the list of dialogs (with all newlines removed) made by character in play.
    >>> file = open('play.txt')
    >>> actual = read_lines(file, 'MARK ANTONY')
    >>> expected = \
    ['I am sorry to give breathing to my purpose,--', \
    'Now, my dearest queen,--', \
    "What's the matter?"]
    >>> actual == expected
    True
    >>> file.close()
    """

    """result = []
    # read the first line, which includes a character's name and first line of dialog
    line = play.readline().strip()
    while line:
        # parse name and dialog
        name = line[1: line.find(']')]
        dialog = line[line.find(']') + 2:]
        # read next line
        line = play.readline().strip()
        # if line is continued dialogue, store in dialogue and continue reading until not
        while line and ']' not in line:
            dialog = dialog + ' ' + line
            line = play.readline().strip()

        # break so not, so then append dialogue if character name is ours
        if name == character:
            result.append(dialog)
        # return result.
    return result"""

def bubble_sort(lst: list) -> None:
    """Sort the items of lst in non-decreasing order, in place.

    >>> lst = [4, 2, 5, 6, 7, 3, 1]
    >>> bubble_sort(lst)
    >>> lst
    [1, 2, 3, 4, 5, 6, 7]
    >>> lst = [5, 2]
    >>> bubble_sort(lst)
    >>> lst
    [2, 5]
    >>> lst = [42]
    >>> bubble_sort(lst)
    >>> lst
    [42]
    >>> lst = []
    >>> bubble_sort(lst)
    >>> lst
    []
    """

    for i in range(len(lst), 1, -1):
        bubble_up(lst, i)
        # print(lst)  # uncomment to see the passes


def bubble_up(lst: list, end: int) -> None:
    """Bubble up the largest element in lst[:end] into index end-1.

    Preconditions: 0 <= end <= len(lst)

    >>> lst = []
    >>> bubble_up(lst, 0)
    >>> lst
    []
    >>> lst = [42]
    >>> bubble_up(lst, 1)
    >>> lst
    [42]
    >>> lst = [4, 2, 5, 6, 7, 3, 1]
    >>> bubble_up(lst, 7)
    >>> lst
    [2, 4, 5, 6, 3, 1, 7]
    >>> lst = [4, 2, 5, 6, 7, 3, 1]
    >>> bubble_up(lst, 5)
    >>> lst
    [2, 4, 5, 6, 7, 3, 1]

    """

    for i in range(1, end):
        if lst[i - 1] > lst[i]:
            lst[i - 1], lst[i] = lst[i], lst[i - 1]  # swap!

from typing import List

def insert(lst: List[int], v: int) -> None:
    """Insert v into lst just before the rightmost item greater than v, or at
    index 0 if no items are greater than v.

    >>> my_list = [3, 10, 4, 2]
    >>> insert(my_list, 5)
    >>> my_list
    [3, 5, 10, 4, 2]
    >>> my_list = [5, 4, 2, 10]
    >>> insert(my_list, 20)
    >>> my_list
    [20, 5, 4, 2, 10]
    """
    # init right most 0 in case none
    rightmost = 0
    # add val to lst
    lst.append(v)
    # find right most greatest INDEX
    for i in range(0, len(lst)-1):
        if lst[i] > v:
            rightmost = i
    # loop backwards, set j-1 to j so that [1,2,3,4] becomes [1,1,2,3]
    for j in range(len(lst)-1, rightmost-1, -1):
        lst[j] = lst[j-1]
    #.set index to v
    lst[rightmost] = v
    
i = 'a'
j = 'b'
print('({1}, {0})'.format(i, j))