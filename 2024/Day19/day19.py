import numpy as np

towel_arrangement_possibilities = 0


def main():
    f = open('example.txt')
    input = f.readlines()
    f.close()

    available_towels = None
    towel_arrangements = []

    for i, line in enumerate(input):
        line = line.strip()
        if i == 0:
            # read available towels
            available_towels = line.split(',')
            available_towels = [t.strip() for t in available_towels]
        elif i == 1:
            continue
        else:
            towel_arrangements.append(line)

    del line, i, input, f
    ##############################################

    # searching for arrangements
    available_towels.sort(key=len)
    available_towels = list(reversed(available_towels))

    arrangement_count = 0
    for i, arrangement in enumerate(towel_arrangements):
        global towel_arrangement_possibilities
        towel_arrangement_possibilities = 0

        print(f'Arrangement #{i + 1}/{len(towel_arrangements)}: {arrangement}')
        arrangeable = search_arrangement(target_arrangement=arrangement,
                                         available_towels=available_towels.copy()
                                         )

        if arrangeable:
            print(f'Can be arranged! Towels: {towel_arrangement_possibilities}')
            arrangement_count += 1
        else:
            print('Arrangement not possible. :(')

    print('\n###################################')
    print(f'Number of arrangements: {arrangement_count}')


def search_arrangement(target_arrangement: str,
                       available_towels: [str],
                       ) -> (bool, [str]):
    target_arrangement = str(target_arrangement)
    available_towels = available_towels.copy()
    global towel_arrangement_possibilities

    # pre checking towels if they are even possible
    possible_towels = []
    for i, towel in enumerate(available_towels):
        if towel in target_arrangement:
            possible_towels.append(towel)

    # print(f'Optimized towel count: {len(available_towels)} -> {len(possible_towels)}')
    available_towels = possible_towels

    # now towels possible?
    if len(available_towels) == 0:
        return False

    # can it even end like this?
    ending_towels = [target_arrangement.endswith(towel) for towel in available_towels]
    endable = any(ending_towels)
    if not endable:
        # cannot even end with the given towels
        return False

    # it there only one possible ending?
    ending_towels = np.array(ending_towels, dtype=bool)
    ending_towels_count = np.count_nonzero(ending_towels)
    if ending_towels_count == 1:
        ending_towel_index = int(np.where(ending_towels)[0])
        ending_towel = available_towels[ending_towel_index]

        # removing the last arrangement
        new_arrangement = target_arrangement[:-len(ending_towel)]
        if len(new_arrangement) > 0:
            # not leaving target arrangement empty.
            # not to mess with the loop
            target_arrangement = new_arrangement

    # searching every available towel if it can produce
    for i, towel in enumerate(available_towels):
        towel = str(towel).strip()

        # if remaining arrangement is fully covered by available towel
        if towel == target_arrangement:
            towel_arrangement_possibilities += 1
            return True

        # can the arrangement start with this towel??
        if target_arrangement.startswith(towel):
            child_arrangement = target_arrangement[len(towel):]
            child_possible = search_arrangement(target_arrangement=child_arrangement,
                                                available_towels=available_towels
                                                )
            if child_possible:
                return True

        # can the arrangement end with this towel??
        if target_arrangement.endswith(towel):
            child_arrangement = target_arrangement[:-len(towel)]
            child_possible = search_arrangement(target_arrangement=child_arrangement,
                                                available_towels=available_towels
                                                )
            if child_possible:
                return True

    # checking if any child can arrange towels
    return False


if __name__ == '__main__':
    main()
