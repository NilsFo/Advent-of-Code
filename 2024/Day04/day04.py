import numpy as np
import pandas as pd

finds = 0
tmp_matrix = []


def main():
    global finds

    f = open('input.txt')
    input = f.read()
    f.close()

    lines = input.split('\n')

    text_matrix = []
    for line in lines:
        line = list(line)
        text_matrix.append(line)

    text_matrix = np.asarray(text_matrix)
    dimensions = text_matrix.shape
    width = dimensions[0]
    height = dimensions[1]

    global tmp_matrix
    tmp_matrix = np.copy(text_matrix)

    for x in range(width):
        for y in range(height):
            search_matrix(text_matrix=text_matrix,
                          x=x, y=y,
                          history='',
                          target_char='X')

    print(f'Original puzzle sequences found: {finds}')

    #####################
    # GOLD STAR
    finds = 0

    for x in range(width):
        for y in range(height):
            current_char = text_matrix[x, y]
            if current_char == 'A':
                search_x_pattern(text_matrix=text_matrix,
                                 x=x, y=y
                                 )

    print(f'Gold star finds: {finds}')


def search_x_pattern(text_matrix: np.ndarray,
                     x: int,
                     y: int
                     ):
    TL = get_if_exists(text_matrix, x - 1, y - 1)
    TR = get_if_exists(text_matrix, x - 1, y + 1)
    BL = get_if_exists(text_matrix, x + 1, y - 1)
    BR = get_if_exists(text_matrix, x + 1, y + 1)

    global finds

    if TL is None or TR is None or BL is None or BR is None:
        return
    if TL == '.' or TR == '.' or BL == '.' or BR == '.':
        return
    if TL == 'A' or TR == 'A' or BL == 'A' or BR == 'A':
        return
    if TL == 'X' or TR == 'X' or BL == 'X' or BR == 'X':
        return

    if TL == BR or BL == TR:
        return

    if True:
        finds += 1
        print(f'################\n'
              f'{TL}.{TR}\n'
              f'.A.\tat({y},{x})\n'
              f'{BL}.{BR}')

        global tmp_matrix
        tmp_matrix[x, y] = '!'


def get_if_exists(text_matrix: np.ndarray,
                  x: int,
                  y: int
                  ) -> str:
    height, width = text_matrix.shape
    if (0 > x or x >= height) or (0 > y or y >= width):
        return None
    return str(text_matrix[x, y])


def search_matrix(text_matrix: np.ndarray,
                  target_char: str,
                  history: str,
                  x: int,
                  y: int,
                  force_dir: () = None):
    global finds

    height, width = text_matrix.shape
    if (0 > x or x >= height) or (0 > y or y >= width):
        return False

    current_char = text_matrix[x, y]
    next_char = next_char_sequence(current_char)

    # check for test input
    if current_char == '.':
        return False
    if current_char == 'X':
        history = f'({x},{y})'
    else:
        history = history + f'->({x},{y})'

    if current_char == target_char:
        # if i found an 'S' in the sequence:
        # SEQUENCE COMPLETE
        if current_char == 'S':
            print(f'SEQUENCE COMPLETE! -> {history}')
            finds += 1
            return True

        if force_dir is None:
            search_matrix(text_matrix, next_char, history, x - 1, y + 0, (-1, 0))  # North
            search_matrix(text_matrix, next_char, history, x + 1, y + 0, (1, 0))  # South
            search_matrix(text_matrix, next_char, history, x + 0, y + 1, (0, 1))  # East
            search_matrix(text_matrix, next_char, history, x + 0, y - 1, (0, -1))  # West
            search_matrix(text_matrix, next_char, history, x - 1, y + 1, (-1, 1))  # North-East
            search_matrix(text_matrix, next_char, history, x - 1, y - 1, (-1, -1))  # North-West
            search_matrix(text_matrix, next_char, history, x + 1, y + 1, (1, 1))  # South-East
            search_matrix(text_matrix, next_char, history, x + 1, y - 1, (1, -1))  # South-West
        else:
            force_x, force_y = force_dir
            search_matrix(text_matrix, next_char, history, x + force_x, y + force_y, force_dir)


def next_char_sequence(current_char) -> str:
    if current_char == 'X':
        return 'M'
    if current_char == 'M':
        return 'A'
    if current_char == 'A':
        return 'S'
    return None


if __name__ == '__main__':
    main()
