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
                1: {7: [1, 7], 5: [0, 6], 3: [0, 7]},
                2: {0: [3, 1], 4: [2, 1], 6: [1, 3]},
                3: {7: [1, 6], 5: [3, 7], 1: [0, 7]},
                4: {2: [2, 1], 0: [0, 3], 6: [1, 1]},
                5: {7: [2, 7], 1: [0, 6], 3: [3, 7]},
                6: {2: [1, 3], 4: [1, 1], 0: [0, 1]},
                7: {1: [1, 7], 5: [2, 7], 3: [1, 6]}}[low][high]
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

class RotationRememberer(object):
    def __init__(self):
        self.seen = {}

    def make_seen(self, pairs):
        first_key = (pairs[0][0],pairs[0][1])
        second_key = (pairs[1][0],pairs[1][1])
        third_key = (pairs[2][0],pairs[2][1])
        if not first_key in self.seen:
            self.seen[first_key] = {}
        if not second_key in self.seen[first_key]:
            self.seen[first_key][second_key] = {}
        self.seen[first_key][second_key][third_key] = True
        return True

    def check_seen(self, pairs):
        unrotate = lambda p, r: ((p[0]-2*r)%8, (p[1]-2*r)%8)
        isomers = [sorted(map(lambda p: tuple(sorted(unrotate(p, i))), pairs)) for i in range(4)]
        for isomer in isomers:
            if self.seen.get(isomer[0]) and \
            self.seen[isomer[0]].get(isomer[1]) and \
            self.seen[isomer[0]][isomer[1]].get(isomer[2]):
                return True
        return False

    def reject_or_make_seen(self, pairs):
        if self.check_seen(pairs):
            return False
        return self.make_seen(pairs)

def filter_wanted_check(list_of_pairs, remove_duplicates, queer):
    output = list_of_pairs
    if remove_duplicates:
        memory = RotationRememberer()
        output = filter(memory.reject_or_make_seen, output)
    if queer:
        pass #later this will remove straight lines
    return output

def all_possible_shape_combinations():
    return all_desired_shape_combinations(False, False)

def all_desired_shape_combinations(remove_duplicates=True, queer=False, debug=False):
    if debug:
        color_picks = [(0,0,0)]
    else:
        color_picks = permutations(COLOR_ENCODING)
    point_orderings = permutations(range(8), 6)
    pairs_orderings = filter(very_sorted, imap(pair_up_list,point_orderings))
    desired_orderings = filter_wanted_check(pairs_orderings, remove_duplicates,
            queer)
    #for i, o in enumerate(desired_orderings):
    #    if i in set([99, 100, 108, 83, 84, 57, 58, 59, 61]):
    #        print "Fails: "+str(o)+str(i*6+1)
    #    elif i in set([98, 99, 100, 101, 107, 109, 82, 83, 84, 85, 56, 57, 58, 59, 60, 62]):
    #        print "Succeeds: "+str(o)+str(i*6+1)
    return [make_line(pairs, colors) for pairs in desired_orderings for
            colors in color_picks]


FILEPATH = "cardlist.txt"

def main():
    lines = open(FILEPATH, "w")
    for line in all_desired_shape_combinations(debug=True):
        lines.write(line)
    lines.close()

if __name__ == "__main__":
    main()
