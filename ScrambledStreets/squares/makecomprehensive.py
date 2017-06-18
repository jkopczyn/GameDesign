#!/usr/bin/python
from itertools import permutations
from itertools import izip
from itertools import imap
from string import digits as DIGITS
import sys
import os

def edges_to_type_and_rotation(low,high):
    parities = [low%2, high%2]
    if parities == [0, 1]:
        rotation = -low/2 % 4
        edgetype = edges_to_type(0, (high - low)%8)
    elif parities == [1, 0]:
        rotation = -high/2 % 4
        edgetype = edges_to_type(0, (low - high)%8)
    else:
        rotation, edgetype = {
                0: {2: [3, 1], 4: [0, 3], 6: [0, 1]},
                1: {7: [3, 7], 5: [0, 6], 3: [0, 7]},
                2: {0: [3, 1], 4: [2, 1], 6: [1, 3]},
                3: {7: [1, 6], 5: [3, 7], 1: [0, 7]},
                4: {2: [2, 1], 0: [0, 3], 6: [1, 1]},
                5: {7: [2, 7], 1: [0, 6], 3: [3, 7]},
                6: {2: [1, 3], 4: [1, 1], 0: [0, 1]},
                7: {1: [3, 7], 5: [2, 7], 3: [1, 6]}}[low][high]
    return map(str,[edgetype, rotation])


def edges_to_type(low, high):
    if low > high:
        low, high = high, low
    lookup = {
            1: {3: '7', 5: '6'},
            0: {7: '0', 6: '1', 5: '2', 4: '3', 3: '4', 1: '5'}}
    return lookup[low][high]

COLOR_ENCODING = [0,1,2]

def make_line(pairs, colors):
    pairwise_typing = lambda x: edges_to_type_and_rotation(*x)
    charblobs = imap(str,izip(imap(pairwise_typing, pairs),colors))
    return ' '.join(c for c in ''.join(charblobs) if c in DIGITS)+'\n'

def pair_up_list(l):
    return list(izip(*[iter(l)]*2))

def very_sorted(lol):
    return sorted(lol) == list(lol) and all(sorted(l) == list(l) for l in lol)

def all_possible_shape_combinations():
    point_orderings = permutations(range(8), 6)
    pairs_orderings = filter(very_sorted, imap(pair_up_list,point_orderings))
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
