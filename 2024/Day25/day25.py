import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from fontTools.misc.cython import returns


class Schematic:

    def __init__(self, schematic_matrix: np.ndarray):
        super().__init__()
        self.schematic_matrix = schematic_matrix

    def is_key(self) -> bool:
        return not all(self.schematic_matrix[0, :])

    def to_sequence(self) -> np.ndarray:
        h, w = self.schematic_matrix.shape

        heights: [int] = []
        for i in range(w):
            column = self.schematic_matrix[:, i]
            heights.append(np.sum(column) - 1)

        # if self.is_key():
        #    heights = [w - h for h in heights]

        return np.array(heights)

    def match(self, other: 'Schematic') -> bool:
        if self.is_key() == other.is_key():
            type = ''
            if self.is_key():
                type = 'KEY'
            else:
                type = 'LOCK'
            raise TypeError(f'Cannot unlock a {type} with another {type}.')

        w, h = self.schematic_matrix.shape
        matching = self.to_sequence() + other.to_sequence()
        return np.all(matching <= h)

    def __repr__(self):
        type = ''
        if self.is_key():
            type = 'KEY'
        else:
            type = 'LOCK'

        return f'Schematic({type} -> {self.to_sequence()})'


def main():
    f = open('input.txt', 'r')
    input = f.readlines()
    f.close()

    schematics: [np.ndarray] = []

    for i in range(0, len(input), 8):
        schematic = []
        for j in range(0, 7):
            line = input[i + j]
            line = line.strip()
            schematic.append(list(line))

        schematic = np.array(schematic, dtype=str)
        schematic = (schematic == '#')
        schematics.append(schematic)

    schematics = [Schematic(s) for s in schematics]

    ###################################
    del f, i, input, j, line, schematic
    ###################################

    keys: [Schematic] = []
    locks: [Schematic] = []
    for schematic in schematics:
        if schematic.is_key():
            keys.append(schematic)
        else:
            locks.append(schematic)

    ##################
    # trying to fit keys into locks
    openings = 0
    for key in keys:
        for lock in locks:
            matches = key.match(lock)
            if matches:
                print(f'Key {key} opens lock {lock}!')
                openings += 1

    print(f'Number of opened locks: {openings}')


if __name__ == '__main__':
    main()
