"""CSC108/A08: Fall 2021 -- Assignment 1: unscramble

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Anya Tafliovich.

"""

# Valid moves in the game.
SHIFT = 'S'
SWAP = 'W'
CHECK = 'C'


# We provide a full solution to this function as an example.
def is_valid_move(move: str) -> bool:
    """Return True if and only if move is a valid move. Valid moves are
    SHIFT, SWAP, and CHECK.

    >>> is_valid_move('C')
    True
    >>> is_valid_move('S')
    True
    >>> is_valid_move('W')
    True
    >>> is_valid_move('R')
    False
    >>> is_valid_move('')
    False
    >>> is_valid_move('NOT')
    False

    """

    return move == CHECK or move == SHIFT or move == SWAP

# Your turn! Provide full solutions to the rest of the required functions.

def get_section_start(section_number: int, section_length: int) -> int:
    """Return the index of the first character in the section number
    section_number with length section_length

    Preconditions: section_number >= 1, section_length >= 1,
                   section_number > 0

    >>> get_section_start(2, 3)
    3
    >>> get_section_start(3, 4)
    8
    >>> get_section_start(5, 2)
    8
    >>> get_section_start(1, 7)
    0
    """

    return (section_number - 1) * section_length

def get_section(game_state: str, section_number: int, section_length:
                int) -> str:
    """Return a string which is the section of game_state that corresponds to
    the given section_number and section_length

    Preconditions: len(gamestate) % section_length == 0,
                   len(game_state) / section_length >= section_number,
                   section_number > 0

    >>> get_section('kitkatbar', 3, 3)
    'bar'
    >>> get_section('broccoli', 1, 4)
    'broc'
    >>> get_section('kitkatbars', 2, 5)
    'tbars'
    >>> get_section('hazelnut', 4, 2)
    'ut'

    """

    section_start = get_section_start(section_number, section_length)
    return game_state[section_start:section_start + section_length]

def is_valid_section(game_state: str, section_number: int, section_length:
                     int) -> bool:
    """Return True if and only if length of game_state game_state is divisible
    by the section length section_length and section number section_number is
    an existing section.

    >>> is_valid_section('nutella', 1, 3)
    False
    >>> is_valid_section('vitamins', 2, 4)
    True
    >>> is_valid_section('hersheys', 3 , 4)
    False
    >>> is_valid_section('tiramisu', 1, 2)
    True
    >>> is_valid_section('tiramisu', 0, 2)
    False
    """

    return (len(game_state) % section_length == 0 and len(game_state)
            / section_length >= section_number and section_number > 0)

def swap(game_state: str, start_index: int, end_index: int) -> str:
    """Return a string which is the result of applying a Swap operation
    to the section of the game state game_state string between starting index
    start_index (inclusive) and ending index end_index (exclusive).

    Preconditions: start_index is a valid index for game_state,
    end_index is a valid index for game_state, start_index < end_index - 1

    >>> swap('peanutbutter', 3, 6)
    'peatunbutter'
    >>> swap('jellybean', 1, 8)
    'jallybeen'
    >>> swap('peanutbutter', 0, 12)
    'reanutbuttep'
    >>> swap('jellybean', 2,4)
    'jellybean'

    """

    swapped = (game_state[:start_index] + game_state[end_index - 1]
               + game_state[start_index + 1:end_index - 1]
               + game_state[start_index] + game_state[end_index:])
    return swapped

def shift(game_state: str, start_index: int, end_index: int) -> str:
    """Return a string which is the result of applying a Shift
    operation to the section of the game state game_state string between
    beginning index start_index (inclusive) and ending index end_index
    (exclusive).

    Preconditions: start_index is a valid index for game_state,
    end_index is a valid index for game_state, start_index < end_index - 1

    >>> shift('cookies', 0, 3)
    'oockies'
    >>> shift('frenchfries', 4, 9)
    'frenhfrices'
    >>> shift('cookies', 0, 7)
    'ookiesc'
    >>> shift('frenchfries', 2, 4)
    'frnechfries'

    """

    shifted = (game_state[:start_index] + game_state[start_index + 1:end_index]
               + game_state[start_index] + game_state[end_index:])
    return shifted

def check(game_state: str, start_index: int, end_index: int, correct_answer:
          str) -> bool:
    """Return True if and only if the part of the game_state game_state string
    between index start_index (inclusive) and index end_index (exclusive) is
    the same as the part of the correct word correct_answer between start index
    start_index (inclusive) and end index end_index (exclusive)

    Preconditions: start_index is a valid index for game_state,
    end_index is a valid index for game_state, start_index <= end_index,
    game_state and correct_answer contain same letters just rearranged

    >>> check('pokcy', 2, 4, 'pocky')
    False
    >>> check('chocotela', 0, 5, 'chocolate')
    True
    >>> check('pocky', 0, 5, 'pocky')
    True
    >>> check('chocolate', 2, 4, 'cchoolate')
    False

    """

    return (game_state[start_index: end_index]
            == correct_answer[start_index: end_index])

def check_section(game_state: str, section_number: int, section_length: int,
                  correct_answer: str) -> bool:
    """Return True if and only if the section of game_state specified by
    section number section_number with length of section_length is equal to the
    section of correct word correct_answer specified by number section_number
    with length of section_length

    Preconditions: len(gamestate) % section_length == 0,
    len(game_state) / section_length >= section_number, section_number < 0
    game_state and correct_answer contain same letters just rearranged

    >>> check_section('ieccream', 1, 4, 'icecream')
    False
    >>> check_section('ieccream', 2, 4, 'icecream' )
    True
    >>> check_section('flauvor', 1, 2, 'flavour')
    True
    >>> check_section('flavuors', 2, 4, 'flavours')
    False

    """

    section_start = get_section_start(section_number, section_length)
    return (check(game_state, section_start, section_start + section_length,
                  correct_answer))

def change_section(game_state: str, move: str, section_number: int,
                   section_length: int) -> str:
    """Return a new game state which results from applying the given game
    move on the section with the given section number.

    Preconditions: len(gamestate) % section_length == 0,
    len(game_state) / section_length >= section_number, move == 'S'
    or move == 'W'

    >>> change_section('lollipops', 'W', 2, 3)
    'lolpilops'
    >>> change_section('bubblegum', 'S', 3, 3)
    'bubbleumg'
    >>> change_section('lollipop', 'S', 2, 2)
    'lollipop'
    >>> change_section('bubblegum', 'W', 1, 3)
    'bubblegum'

    """

    section_start = get_section_start(section_number, section_length)
    section_end = section_start + section_length
    if move == SHIFT:
        return shift(game_state, section_start, section_end)
    return swap(game_state, section_start, section_end)


def get_move_hint(game_state: str, section_number: int, section_length: int,
                  correct_answer: str) -> str:
    """Return shift move suggestion if section of current game state, game_state
    with section number, section_number with length, section_length will be the
    same as corresponding section in the correct word, correct_answer after
    being shifted once, or twice. Return swap move suggestion otherwise.

    Preconditions: len(gamestate) % section_length == 0,
    len(game_state) / section_length >= section_number,
    game_state and correct_answer contain same letters just rearranged

    >>> get_move_hint('ubblbeegum', 2, 3, 'bubblegum')
    'W'
    >>> get_move_hint('gomanjuice', 1, 5, 'mangojuice')
    'S'
    >>> get_move_hint('imveryryhung', 2, 6, 'imveryhungry')
    'S'
    >>> get_move_hint('nonmomnom', 2, 2, 'nomnomnom')
    'S'

    """

    shift_once = (change_section(game_state, SHIFT, section_number,
                                 section_length))
    shift_twice = (change_section(shift_once, SHIFT, section_number,
                                  section_length))

    if (check_section(shift_once, section_number, section_length,
                      correct_answer)
            or check_section(shift_twice, section_number, section_length,
                             correct_answer)):
        return SHIFT
    return SWAP

if __name__ == '__main__':
    import doctest
    doctest.testmod()
