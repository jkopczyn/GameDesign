#!python2

# Create a cardlist file based on constraints specified

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

def no_straights_allowed(ordering):
    for pair in ordering:
        if pair in [(0, 5), (1,4), (2, 7), (3, 6)]:
            return False
    return True

def crossed_lines_only(pairs):
    #not sure what to do for this. wide curves cross each other, lines split
    #   the land and pairs that cross that cross them.
    biglookuphash = {(0,1): [], (1,2): [], (2,3): [], (3,4): [],
            (4,5): [], (5,6): [], (6,7): [], (0, 7): [],
            (0,2): [tuple(sorted((1, n))) for n in range(8)],
            (1,3): [tuple(sorted((2, n))) for n in range(8)],
            (2,4): [tuple(sorted((3, n))) for n in range(8)],
            (3,5): [tuple(sorted((4, n))) for n in range(8)],
            (4,6): [tuple(sorted((5, n))) for n in range(8)],
            (5,7): [tuple(sorted((6, n))) for n in range(8)],
            (0,6): [tuple(sorted((7, n))) for n in range(8)],
            (1,7): [tuple(sorted((0, n))) for n in range(8)],
            (0,3): [tuple(sorted((x,y))) for x in  [1,2] for y in range(4,8)] +
                [(4,7)],
            (1,4): [tuple(sorted((x,y))) for x in  [2,3] for y in (
                [0]+range(5,8))] +[(0,5)],
            (2,5): [tuple(sorted((x,y))) for x in  [3,4] for y in (
                [0,1]+range(6,8))] +[(1,6)],
            (3,6): [tuple(sorted((x,y))) for x in  [4,5] for y in (
                range(3)+[7])] +[(2,7)],
            (4,7): [tuple(sorted((x,y))) for x in  [5,6] for y in range(4)] +
                [(0,3)],
            (0,5): [tuple(sorted((x,y))) for x in  [6,7] for y in range(1,5)] +
                [(1,4)],
            (1,6): [tuple(sorted((x,y))) for x in  [0,7] for y in range(2,6)] +
                [(2,5)],
            (2,7): [tuple(sorted((x,y))) for x in  [0,1] for y in range(3,7)] +
                [(3,6)],
            (0,4): [tuple(sorted((x,y))) for x in [1,2,3] for y in [5,6,7]],
            (1,5): [tuple(sorted((x,y))) for x in [2,3,4] for y in [0,6,7]],
            (2,6): [tuple(sorted((x,y))) for x in [3,4,5] for y in [0,1,7]],
            (3,7): [tuple(sorted((x,y))) for x in [4,5,6] for y in [0,1,2]]
            }
    is_crossed = lambda p: any(q in pairs for q in biglookuphash[p])
    return any(map(is_crossed, pairs))


def filter_wanted_check(list_of_pairs, remove_duplicates, queer, disorderly):
    output = list_of_pairs
    if remove_duplicates:
        memory = RotationRememberer()
        output = filter(memory.reject_or_make_seen, output)
    if queer:
        output = filter(no_straights_allowed, output)
    if disorderly:
        output = filter(crossed_lines_only, output)
    return output

def all_possible_shape_combinations():
    return all_desired_shape_combinations(False, False)

def all_desired_shape_combinations(remove_duplicates=True, queer=False, disorderly=False, debug=False):
    if debug:
        color_picks = [(0,0,0)]
    else:
        color_picks = permutations(COLOR_ENCODING)
    point_orderings = permutations(range(8), 6)
    pairs_orderings = filter(very_sorted, imap(pair_up_list,point_orderings))
    desired_orderings = filter_wanted_check(pairs_orderings, remove_duplicates,
            queer, disorderly)
    return [make_line(pairs, colors) for pairs in desired_orderings for
            colors in color_picks]


FILEPATH = "cardlist.txt"

def main(outpath=None, bitmap=7):
    debug, queer, disorderly = (bool(x) for x in (bitmap&4, bitmap&2, bitmap&1))
    if not outpath:
        outpath = FILEPATH
    lines = open(outpath, "w")
    for line in all_desired_shape_combinations(debug=debug, queer=queer, disorderly=disorderly):
        lines.write(line)
    lines.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        n, s = sorted(sys.argv[1:], key=lambda x: len(x))
        try:
            n = int(n)
            if n > 7 or n < 0:
                print("Bad args, should be int 0-7 and/or filename")
                exit
        except ValueError:
            print("Bad args, should be int 0-7 and/or filename")
            exit
        main(bitmap=n, outpath=s)
        if len(sys.argv[1]) > 1:
            file = sys.argv[1]
        elif len(sys.argv[2]) > 1:
            file = sys.argv[2]
        else:
            print("Bad args, should be int 0-7 and/or filename")
            exit
    elif len(sys.argv) == 2:
        if len(sys.argv[1]) > 1:
            main(outpath=sys.argv[1])
        else:
            try:
                bitmap = int(sys.argv[1])
                if bitmap > 7 or bitmap < 0:
                    print("Bad args, should be int 0-7 and/or filename")
                main(bitmap=bitmap)
            except ValueError:
                print("Bad args, should be int 0-7 and/or filename")
    elif len(sys.argv) > 3:
            print("Bad args, should be int 0-7 and/or filename")
    else:
        main()
