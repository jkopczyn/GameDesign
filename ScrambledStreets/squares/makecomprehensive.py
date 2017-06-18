#!/usr/bin/python
from itertools import permutations
from itertools import izip
from itertools import imap
from string import digits as DIGITS
import sys
import os

def edges_to_type_and_rotation(low,high):
    parities = [low%2, high%2]
    if parities == [1, 0]:
        rotation = -(low - 1)/2 % 4
        edgetype = edges_to_type(0, (high - low)%8)
    elif parities == [0, 1]:
        rotation = -(high - 1)/2 % 4
        edgetype = edges_to_type(0, (low - high)%8)
    else:
        rotation, edgetype = {
                0: {2: [3, 2], 4: [0, 4], 6: [0, 2]},
                1: {7: [3, 8], 5: [0, 7], 3: [0, 8]},
                2: {0: [3, 2], 4: [2, 2], 6: [1, 4]},
                3: {7: [1, 7], 5: [3, 8], 1: [0, 8]},
                4: {2: [2, 2], 0: [0, 4], 6: [1, 2]},
                5: {7: [2, 8], 1: [0, 7], 3: [3, 8]},
                6: {2: [1, 4], 4: [1, 2], 0: [0, 2]},
                7: {1: [3, 8], 5: [2, 8], 3: [1, 7]}}[low][high]
    return [rotation, edgetype]


def edges_to_type(low, high):
    if low > high:
        low, high = high, low
    lookup = {
            1: {3: '8', 5: '7'},
            0: {7: '1', 6: '2', 5: '3', 4: '4', 3: '5', 1: '6'}}
    return lookup[low][high]

COLOR_ENCODING = [0,1,2]

def make_line(pairs, colors):
    pairwise_typing = lambda x: edges_to_type_and_rotation(*x)
    charblobs = imap(str,izip(imap(pairwise_typing, pairs),colors))
    return ' '.join(c for c in ''.join(charblobs) if c in DIGITS)+'\n'

def pair_up_list(l):
    return list(izip(*[iter(l)]*2))

def all_possible_shape_combinations():
    point_orderings = permutations(range(8), 6)
    y = list(imap(pair_up_list,point_orderings))
    print y[:3]
    pairs_orderings = filter(
            lambda x: sorted(x)==x,
            y
            )
    return [make_line(pairs, colors) for pairs in pairs_orderings for
            colors in permutations(COLOR_ENCODING)]


FILEPATH = "cardlist.txt"

def main():
    lines = open(FILEPATH, "w")
    for line in all_possible_shape_combinations():
        lines.write(line)
    lines.close()

if __name__ == "__main__":
    main()
