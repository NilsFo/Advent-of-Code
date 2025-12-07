import numpy as np


def main():
    f = 'example.txt'
    f = open(f)
    lines = f.readlines()
    f.close()

    ############################################

    max_length = max([len(l) for l in lines])
    input_map = np.full((len(lines), max_length - 1), '')

    for i, line in enumerate(lines):
        line = line.rstrip()

        for j, char in enumerate(line):
            input_map[i, j] = char.strip()

    ############################################

    start_pos = np.where(input_map == 'S')
    start_pos = (int(start_pos[0]), int(start_pos[1]))

    splitter_mask = input_map == '^'
    beam_mask = np.zeros(input_map.shape, dtype=np.bool)
    beam_mask[start_pos] = True

    ############################################
    part_1(input_map, beam_mask, splitter_mask)
    ############################################
    part_2(input_map, beam_mask, splitter_mask)
    ############################################


def part_2(input_map, beam_mask, splitter_mask):
    pass


def part_1(input_map, beam_mask, splitter_mask):
    splits_count = 0
    input_map = input_map.copy()
    beam_mask = beam_mask.copy()
    splitter_mask = splitter_mask.copy()

    for i in range(input_map.shape[0] - 1):
        current_beam_row = beam_mask[i, :]
        next_splitter_row = splitter_mask[i + 1, :]
        current_beam_indices = np.where(current_beam_row)

        for beam_index in current_beam_indices[0]:
            beam_index = int(beam_index)

            if next_splitter_row[beam_index]:
                beam_mask[i + 1, beam_index - 1] = True
                beam_mask[i + 1, beam_index + 1] = True
                splits_count += 1
            else:
                beam_mask[i + 1, beam_index] = True

    print(f'Splits count: {splits_count}')


if __name__ == '__main__':
    main()
