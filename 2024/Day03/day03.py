import math
from mailbox import ExternalClashError

import numpy as np
import pandas as pd
import re

pattern = 'mul\((\d+),(\d+)\)'


def main():
    f = open('input.txt', 'r')
    puzzle_input = f.read()
    f.close()

    do_indices = [0]
    do_indices.extend([m.start() for m in re.finditer(pattern='do\(\)', string=puzzle_input)])
    dont_indices = [m.start() for m in re.finditer(pattern='don\'t\(\)', string=puzzle_input)]

    result = 0

    p = re.compile(pattern=pattern)
    for i, match in enumerate(p.finditer(puzzle_input)):
        start = match.start()
        closest_do, closest_dont = search_lists(do_indices, dont_indices, start)
        enabled = closer_to(v=start, do=closest_do, dont=closest_dont)
        print(f'Mul index: {start}. Closest do(): {closest_do}. Closest dont(): {closest_dont}. Enabled: {enabled}')

        groups = match.groups()
        left_number = int(groups[0])
        right_number = int(groups[1])

        if right_number < 1000 and left_number < 1000:
            mul = right_number * left_number
            print(f'mult #{i}: {left_number} * {right_number} = {mul}')

            if enabled:
                result += mul

    print(f'Result: {result}')


def closer_to(v: int, do: int, dont: int):
    # closer to 'do' value?
    if abs(v - do) < abs(v - dont):
        return True

    # closer to 'don't' vlaue
    elif abs(v - do) > abs(v - dont):
        return False

    # they are equal?? how?
    else:
        raise ExternalClashError(f'The values are equal: {v}')


def search_lists(do_indices: [int], dont_indices: [int], target: int):
    closest_do = math.inf
    closest_dont = math.inf

    for do in do_indices:
        if do < target:
            closest_do = do

    for dont in dont_indices:
        if dont < target:
            closest_dont = dont

    return closest_do, closest_dont


if __name__ == '__main__':
    main()
