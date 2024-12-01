import os

import pandas as pd
import numpy as np


def main():
    data = pd.read_csv('input.txt', delimiter='   ', header=None)
    left = data[0]
    right = data[1]

    left = list(left)
    right = list(right)
    left.sort()
    right.sort()

    counts = {}
    distance = 0
    for l, r in zip(left, right):
        d = abs(l - r)
        distance += d

        counts[l] = 0
        for k in right:
            if l == k:
                counts[l] += 1

    similarities = 0
    for l in left:
        similarities += l * counts[l]

    print(distance)
    print(similarities)


if __name__ == '__main__':
    main()
