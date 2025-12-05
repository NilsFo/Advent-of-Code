import numpy as np


def main():
    f = 'input.txt'
    f = open(f)
    lines = f.readlines()
    f.close()

    ############################################################
    ranges = []
    ingredients = []

    range_mode = True
    for l in lines:
        l = l.strip()

        if l == '':
            range_mode = False
            continue

        if range_mode:
            value_min, value_max = l.split('-')
            ranges.append((int(value_min), int(value_max)))
        else:
            ingredients.append(int(l))

    fresh_count = 0
    for ingredient in ingredients:
        if is_fresh(ranges, ingredient):
            fresh_count += 1

    print(f'Fresh ingredients in the list: {fresh_count}.')

    ########################################################################
    # DAY 2
    del fresh_count, f, ingredient, range_mode, l, value_max, value_min, lines, ingredients
    ########################################################################

    range_bounds = []
    for r in ranges:
        range_bounds.append(r[0])
        range_bounds.append(r[1])
    del r

    range_min = np.min(range_bounds)
    range_max = np.max(range_bounds)

    merge_able = True
    separate_ranges = []

    while len(ranges) > 0:
        current_range = ranges[0]
        ranges = ranges[1:]

        hit_index = None
        for i in range(len(ranges)):
            if range_overlap(current_range, ranges[i]) and hit_index is None:
                hit_index = i

        if hit_index is None:
            separate_ranges.append(current_range)
        else:
            new_range = merge_ranges(current_range, ranges[hit_index])
            del ranges[hit_index]
            ranges.append(new_range)

    ########################################################################
    separate_indices = 0
    for r in separate_ranges:
        separate_indices += r[1] - r[0] + 1

    print(f'Separate indices: {separate_indices}.')


def range_overlap(a, b):
    return a[0] <= b[1] and b[0] <= a[1]


def merge_ranges(a, b):
    return (
        min((min(a), min(b))),
        max((max(a), max(b)))
    )


def is_fresh(ranges, ingredient):
    for range in ranges:
        if range[0] <= ingredient <= range[1]:
            return True

    return False


if __name__ == '__main__':
    main()

# too high: 352681648086161
