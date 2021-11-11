"""CSC108/A08: Fall 2021 -- Assignment 2: voting

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Sophia Huynh, Sadia Sharmin,
Elizabeth Patitsas, Anya Tafliovich.

"""

from typing import Collection, List

from constants import (COL_RIDING, COL_VOTER, COL_RANK, COL_RANGE,
                       COL_APPROVAL, APPROVAL_TRUE, APPROVAL_FALSE,
                       SEPARATOR)

# In the following docstrings, 'VoteData' refers to a list of 5
# elements of the following types:
#
# at index COL_RIDING: int         (this is the riding number)
# at index COL_VOTER: int         (this is the voter number)
# at index COL_RANK: List[str]   (this is the rank ballot)
# at index COL_RANGE: List[int]   (this is the range ballot)
# at index COL_APPROVAL: List[bool]  (this is the approval ballot)

###############################################################################
# Task 0: Creating example data
###############################################################################

SAMPLE_DATA_1 = [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
                  [False, True, False, False]],
                 [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
                  [False, False, True, True]],
                 [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
                  [False, True, False, True]],
                 [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
                  [True, False, True, True]]]
SAMPLE_ORDER_1 = ['CPC', 'GREEN', 'LIBERAL', 'NDP']


SAMPLE_DATA_2 = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [4, 0, 5, 0],
                  [True, False, True, False]],
                 [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [4, 5, 5, 5],
                  [True, True, True, True]],
                 [72, 12, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [0, 1, 1, 5],
                  [False, True, True, True]]]
SAMPLE_ORDER_2 = ['CPC', 'GREEN', 'LIBERAL', 'NDP']


SAMPLE_DATA_3 = [[28, 3, ['DEMOCRATIC', 'REPUBLICAN'], [8, 2], [True, False]],
                 [3, 3, ['REPUBLICAN', 'DEMOCRATIC'], [4, 5], [True, True]],
                 [49, 35, ['REPUBLICAN', 'DEMOCRATIC'], [0, 1], [False, False]]]
SAMPLE_ORDER_3 = ['DEMOCRATIC', 'REPUBLICAN']

SAMPLE_DATA_4 = [[4, 8, ['CCP'], [0], [False]],
                 [4, 14, ['CCP'], [1], [False]],
                 [13, 8, ['CCP'], [0], [False]]]
SAMPLE_ORDER_4 = ['CCP']


###############################################################################
# Task 1: Data cleaning
###############################################################################

def clean_data(data: List[List[str]]) -> None:
    """Modify data so that the applicable string values are converted to
    their appropriate type, making data of type List['VoteType'].

    Pre: Each item in data is in the format
     at index COL_RIDING: a str that can be converted to an integer (riding)
     at index COL_VOTER: a str that can be converted to an integer (voter ID)
     at index COL_RANK: a SEPARATOR-separated non-empty string (rank ballot)
     at index COL_RANGE: a SEPARATOR-separated non-empty string of ints
                         (range ballot)
     at index COL_APPROVAL: a SEPARATOR-separated non-empty string of
                         APPROVAL_TRUE's and APPROVAL_FALSE's (approval ballot)

    >>> data = [['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']]
    >>> expected = [[0, 1, ['NDP', 'Liberal', 'Green', 'CPC'], [1, 4, 2, 3],
    ...             [False, True, False, False]]]
    >>> clean_data(data)
    >>> data == expected
    True
    >>> data2 = [['2', '15', 'DEMOCRATIC;REPUBLICAN', '10;0', 'YES;NO']]
    >>> expected2 = [[2, 15, ['DEMOCRATIC', 'REPUBLICAN'], [10, 0],
    ...              [True, False]]]
    >>> clean_data(data2)
    >>> data2 == expected2
    True
    >>> data3 = []
    >>> expected3 = []
    >>> clean_data(data3)
    >>> data3 == expected3
    True
    """

    for vote in data:
        vote[COL_RIDING] = int(vote[COL_RIDING])
        vote[COL_VOTER] = int(vote[COL_VOTER])

        vote[COL_RANK] = vote[COL_RANK].split(SEPARATOR)
        vote[COL_RANGE] = vote[COL_RANGE].split(SEPARATOR)
        vote[COL_APPROVAL] = vote[COL_APPROVAL].split(SEPARATOR)

        for value in vote[COL_RANGE]:
            index = vote[COL_RANGE].index(value)
            vote[COL_RANGE][index] = int(vote[COL_RANGE][index])

        for approval in vote[COL_APPROVAL]:
            index = vote[COL_APPROVAL].index(approval)
            vote[COL_APPROVAL][index] = approval == APPROVAL_TRUE

###############################################################################
# Task 2: Data extraction
###############################################################################

def extract_column(data: List[list], column: int) -> list:
    """Return a list containing only the elements at index column for each
    sublist in data.

    Pre: each sublist of data has an item at index column.

    >>> extract_column([[1, 2, 3], [4, 5, 6]], 2)
    [3, 6]
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> extract_column(ballots, 0)
    ['LIBERAL', 'CPC', 'NDP']
    """

    extracted = []
    for sublist in data:
        extracted.append(sublist[column])

    return extracted


def extract_single_ballots(data: List['VoteData']) -> List[str]:
    """Return a list containing only the highest ranked candidate from
    each rank ballot in voting data data.

    Pre: data is a list of valid 'VoteData's
         The rank ballot is at index COL_RANK for each voter.

    >>> extract_single_ballots(SAMPLE_DATA_1)
    ['NDP', 'LIBERAL', 'GREEN', 'LIBERAL']
    """

    extracted = extract_column(data, COL_RANK)
    return extract_column(extracted, 0)

def get_votes_in_riding(data: List['VoteData'],
                        riding: int) -> List['VoteData']:
    """Return a list containing only voting data for riding riding from
    voting data data.

    Pre: data is a list of valid 'VoteData's

    >>> expected = [[1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
    ...              [False, False, True, True]],
    ...             [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
    ...              [False, True, False, True]],
    ...             [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
    ...              [True, False, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_1, 1) == expected
    True
    """

    riding_votes = []

    for vote in data:
        if vote[COL_RIDING] == riding:
            riding_votes.append(vote)

    return riding_votes


###############################################################################
# Task 3.1: Plurality Voting System
###############################################################################

def voting_plurality(single_ballots: List[str],
                     party_order: List[str]) -> List[int]:
    """Return the total number of ballots cast for each party in
    single-candidate ballots single_ballots, in the order specified in
    party_order.

    Pre: each item in single_ballots appears in party_order

    >>> voting_plurality(['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC'],
    ...                  SAMPLE_ORDER_1)
    [1, 3, 0, 1]
    """

    total_ballots = []

    for party in party_order:
        total_ballots.append(single_ballots.count(party))

    return total_ballots


###############################################################################
# Task 3.2: Approval Voting System
###############################################################################

# Note: even though the only thing we need from party_order in this
# function is its length, we still design all voting functions to
# receive party_order, for consistency and readability.
def voting_approval(approval_ballots: List[List[bool]],
                    party_order: List[str]) -> List[int]:
    """Return the total number of approvals for each party in approval
    ballots approval_ballots, in the order specified in party_order.

    Pre: len of each sublist of approval_ballots is len(party_order)
         the approvals in each ballot are specified in the order of party_order

    >>> voting_approval([[True, True, False, False],
    ...                  [False, False, False, True],
    ...                  [False, True, False, False]], SAMPLE_ORDER_1)
    [1, 2, 0, 1]
    """

    approvals = []

    for i in range(len(party_order)):
        num_approvals = 0
        for ballot in approval_ballots:
            if ballot[i]:
                num_approvals += 1
        approvals.append(num_approvals)

    return approvals


###############################################################################
# Task 3.3: Range Voting System
###############################################################################

def voting_range(range_ballots: List[List[int]],
                 party_order: List[str]) -> List[int]:
    """Return the total score for each party in range ballots
    range_ballots, in the order specified in party_order.

    Pre: len of each sublist of range_ballots is len(party_order)
         the scores in each ballot are specified in the order of party_order

    >>> voting_range([[1, 3, 4, 5], [5, 5, 1, 2], [1, 4, 1, 1]],
    ...              SAMPLE_ORDER_1)
    [7, 12, 6, 8]
    """

    total_scores = []

    for i in range(len(party_order)):
        score = 0
        for ballot in range_ballots:
            score += ballot[i]
        total_scores.append(score)

    return total_scores


###############################################################################
# Task 3.4: Borda Count Voting System
###############################################################################

def voting_borda(rank_ballots: List[List[str]],
                 party_order: List[str]) -> List[int]:
    """Return the Borda count for each party in rank ballots rank_ballots,
    in the order specified in party_order.

    Pre: each ballot contains all and only elements of party_order

    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...               ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...               ['LIBERAL', 'NDP', 'GREEN', 'CPC']], SAMPLE_ORDER_1)
    [4, 4, 8, 2]
    """

    borda_counts = []

    for party in party_order:
        count = 0
        for ballot in rank_ballots:
            count += len(party_order) - (ballot.index(party) + 1)
        borda_counts.append(count)

    return borda_counts


###############################################################################
# Task 3.5: Instant Run-off Voting System
###############################################################################

def remove_party(rank_ballots: List[List[str]], party_to_remove: str) -> None:
    """Change rank ballots rank_ballots by removing the party
    party_to_remove from each ballot.

    Pre: party_to_remove is in all of the ballots in rank_ballots.

    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> remove_party(ballots, 'NDP')
    >>> ballots == [['LIBERAL', 'GREEN', 'CPC'],
    ...             ['CPC', 'LIBERAL', 'GREEN'],
    ...             ['CPC', 'GREEN', 'LIBERAL']]
    True
    """

    for ballot in rank_ballots:
        ballot.remove(party_to_remove)

def get_lowest(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the lowest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_lowest([16, 100, 4, 200], SAMPLE_ORDER_1)
    'LIBERAL'
    """

    lowest = party_tallies[0]
    for tally in party_tallies:
        if tally <= lowest:
            lowest = tally

    return party_order[party_tallies.index(lowest)]


def get_winner(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the highest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_winner([16, 100, 4, 200], SAMPLE_ORDER_1)
    'NDP'
    """

    highest = party_tallies[0]
    for tally in party_tallies:
        if tally >= highest:
            highest = tally

    return party_order[party_tallies.index(highest)]


def voting_irv(rank_ballots: List[List[str]], party_order: List[str]) -> str:
    """Return the party which wins when IRV is performed on the list of
    rank ballots rank_ballots. Change rank_ballots and party_order as
    needed in IRV, removing parties that are eliminated in the
    process. Each ballot in rank_ballots is ordered by party_order.

    Pre: each ballot contains all and only elements of party_order
         len(rank_ballots) > 0

    >>> order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]

    >>> voting_irv(ballots, order)
    'NDP'
    >>> ballots == [['LIBERAL', 'NDP'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['NDP', 'LIBERAL']]
    True

    >>> ballots
    [['LIBERAL', 'NDP'], ['NDP', 'LIBERAL'], ['NDP', 'LIBERAL']]
    >>> order
    ['LIBERAL', 'NDP']
    """

    singles = extract_column(rank_ballots, 0)
    singles_count = voting_plurality(singles, party_order)
    winner = get_winner(singles_count, party_order)

    total_votes = 0

    for party in party_order:
        total_votes += singles_count[party_order.index(party)]

    highest = singles_count[party_order.index(winner)]

    while highest <= total_votes - highest:
        lowest = get_lowest(singles_count, party_order)
        remove_party(rank_ballots, lowest)
        party_order.remove(lowest)

        singles = extract_column(rank_ballots, 0)
        singles_count = voting_plurality(singles, party_order)
        winner = get_winner(singles_count, party_order)

        total_votes = 0

        for party in party_order:
            total_votes += singles_count[party_order.index(party)]

        highest = singles_count[party_order.index(winner)]

    return winner

if __name__ == '__main__':
    import doctest
    doctest.testmod()
