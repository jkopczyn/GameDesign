#!/usr/bin/python
from itertools import permutations
import sys
import os

def edges_to_type_and_rotation(low,high):
    parities = [low%2, high%2]
    if parities = [1, 0]:
        rotation = -(low - 1)/2 % 4
        edgetype = edges_to_type(1, (high - (low - 1))%8)
    elif parities = [0, 1]:
        rotation = -(high - 1)/2 % 4
        edgetype = edges_to_type(1, (low - (high - 1))%8)
    else:
        rotation, edgetype = {
                1: {3: [3, 2], 5: [0, 4], 7: [0, 2]},
                2: {8: [3, 8], 6: [0, 7], 4: [0, 8]},
                3: {1: [3, 2], 5: [2, 2], 7: [1, 4]},
                4: {8: [1, 7], 6: [3, 8], 2: [0, 8]},
                5: {3: [2, 2], 1: [0, 4], 7: [1, 2]},
                6: {8: [2, 8], 2: [0, 7], 4: [3, 8]},
                7: {3: [1, 4], 5: [1, 2], 1: [0, 2]},
                8: {2: [3, 8], 6: [2, 8], 4: [1, 7]}}[low][high]
    return [rotation, edgetype]


def edges_to_type(low, high):
    if low > high:
        low, high = high, low
    lookup = {
            2: {4: '8', 6: '7'}, 
            1: {8: '1', 7: '2', 6: '3', 5: '4', 4: '5', 0: '1'}}
    return lookup[low][high]
