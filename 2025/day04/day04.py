import numpy as np


def main():
    f = 'input.txt'
    f = open(f)
    lines = f.readlines()
    f.close()

    rolls_map = np.zeros((len(lines[0].strip()), len(lines)), dtype=np.uint8)

    for i in range(rolls_map.shape[0]):
        for j in range(rolls_map.shape[1]):
            char = lines[i][j]

            if char == '@':
                rolls_map[i, j] = 1

    # ==========================================================

    removing = True
    rounds_count = 0
    removed_count = 0

    while removing:
        rounds_count += 1
        accessible_papers = []

        for i in range(rolls_map.shape[0]):
            for j in range(rolls_map.shape[1]):
                tile = rolls_map[i][j]

                if tile == 1:
                    acs = is_accessible(rolls_map, i, j)
                    if acs:
                        accessible_papers.append((i, j))
                    else:
                        pass

        removing = len(accessible_papers) > 0
        for paper in accessible_papers:
            rolls_map[paper] = 0
            removed_count += 1

    print(removed_count)


def is_accessible(rolls_map, x, y):
    tile = rolls_map[x][y]

    # if x == 0 or y == 0:
    #     return True
    # if x == rolls_map.shape[0] - 1 or y == rolls_map.shape[1] - 1:
    #     return True

    adjacent_tiles = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue

            x_offset = x + i
            y_offset = y + j

            if 0 <= x_offset < rolls_map.shape[0]:
                if 0 <= y_offset < rolls_map.shape[1]:
                    adjacent_tiles.append(rolls_map[x_offset][y_offset])

    return np.sum(adjacent_tiles) < 4


if __name__ == '__main__':
    main()
