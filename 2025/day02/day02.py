import numpy as np

global invalid_ids
invalid_ids = []


def main():
    f = 'input.txt'
    f = open(f)

    ids_raw = f.read()

    f.close()

    ################################################

    id_pairs = []
    for s in ids_raw.split(','):
        s = s.split('-')
        id_pairs.append(
            (int(s[0]), int(s[1]))
        )

    invalid_id_sum = 0
    for pair in id_pairs:
        check_ids(pair[0], pair[1])

    for id in invalid_ids:
        invalid_id_sum += int(id)

    print(f'Sum: {np.sum(invalid_id_sum)}')


def check_ids(lower, upper):
    invalid_ids_local = []

    for id in range(lower, upper + 1):
        is_invalid = check_id_part2(id)

        if is_invalid:
            invalid_ids_local.append(int(id))

    print(f'The range {lower}-{upper} has {len(invalid_ids_local)} ID(s): {invalid_ids_local}')


def check_id_part1(id) -> bool:
    id = str(id)
    l = len(id)

    left_half = id[:l // 2]
    right_half = id[l // 2:]

    if not l % 2 == 0:
        return False

    if int(left_half) == int(right_half):
        # print(f'Turns out, "{left_half}" is equal to "{right_half}". As such, "{id}" is invalid.')
        invalid_ids.append(id)
        return True
    return False


def check_id_part2(id):
    id = str(id)
    l = len(id)
    l_half = l // 2

    for i in range(1, l_half + 1):
        sequence = id[:i]

        if sequence == id:
            continue

        repeats_needed = (len(id)//len(sequence))
        repeated_sequence = sequence * repeats_needed

        if repeated_sequence == id:
            invalid_ids.append(id)
            return True

    return False


if __name__ == '__main__':
    main()
