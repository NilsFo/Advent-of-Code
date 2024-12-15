import numpy as np


def main():
    f = open('input.txt', 'r')
    input = f.readlines()
    f.close()

    height_map = []
    for i, line in enumerate(input):
        line = line.strip()
        heights = []
        for j, char in enumerate(line):
            heights.append(int(char))

        height_map.append(heights)

    height_map = np.array(height_map, dtype=np.uint8)
    del i, j, input, heights, line, f, char
    print('Input Height Map:')
    print_height_map(height_map)

    trail_starts = np.where(height_map == 0)
    trail_starts = list(zip(trail_starts[0], trail_starts[1]))
    print(f'Number of trail starts: {len(trail_starts)}.\nList of trails: {trail_starts}')

    score = 0
    for i, trail_start in enumerate(trail_starts):
        trail_start = (int(trail_start[0]), int(trail_start[1]))

        trail_mask = np.zeros(height_map.shape, dtype=np.bool)
        trail_ends, trail_mask = explore_trail(
            height_map=height_map,
            current_trail_mask=trail_mask,
            current_position=trail_start,
            trail_ends=[]
        )

        print(f'{len(trail_ends)} trail ends for {trail_start}: {trail_ends}')
        print_height_map(height_map=height_map, trail_mask=trail_mask)
        score = score + len(trail_ends)

    print(f'Score: {score}')


def explore_trail(height_map: np.ndarray,
                  current_trail_mask: np.ndarray,
                  current_position: (int, int),
                  trail_ends: [(int, int)]
                  ):
    current_elevation: int = height_map[current_position]
    next_elevation: int = current_elevation + 1
    current_trail_mask[current_position] = True

    # Checking if trail end is reached
    if current_elevation == 9:
        #if current_position not in trail_ends:
        trail_ends.append(current_position)
        return trail_ends, current_trail_mask

    ##################
    # Searching trail
    other_positions = [
        position_offset(current_position=current_position, height_map=height_map, offset_x=0, offset_y=1),  # south
        position_offset(current_position=current_position, height_map=height_map, offset_x=0, offset_y=-1),  # north
        position_offset(current_position=current_position, height_map=height_map, offset_x=1, offset_y=0),  # east
        position_offset(current_position=current_position, height_map=height_map, offset_x=-1, offset_y=0)  # west
    ]

    # removing nons
    other_positions = [p for p in other_positions if p is not None]
    for other_position in other_positions:
        if height_map[other_position] == next_elevation:
            # recursion
            trail_ends, current_trail_mask = explore_trail(height_map=height_map,
                                                           current_trail_mask=current_trail_mask,
                                                           current_position=other_position,
                                                           trail_ends=trail_ends)

    return trail_ends, current_trail_mask


def position_offset(current_position: (int, int), height_map: np.ndarray, offset_x: int, offset_y: int):
    other_position = (
        int(current_position[0] + offset_x),
        int(current_position[1] + offset_y)
    )
    width, height = height_map.shape

    if 0 <= other_position[0] < width and 0 <= other_position[1] < height:
        return other_position
    return None


def print_height_map(height_map: np.ndarray, trail_mask: np.ndarray = None):
    print('')
    for i in range(height_map.shape[0]):
        for j in range(height_map.shape[1]):
            map_character = height_map[i, j]

            if trail_mask is not None and trail_mask[i, j]:
                map_character = '#'

            print(map_character, end='')
        print('\n', end='')
    print('')


if __name__ == '__main__':
    main()
