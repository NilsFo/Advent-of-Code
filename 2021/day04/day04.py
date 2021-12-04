import os

import numpy as np


def main():
    boards, numbers_drawn = get_input()
    stamps = [np.zeros(b.shape, dtype=np.bool) for b in boards]
    winning_board = None
    winning_stamps = None
    winning_number = None

    assert len(boards) == len(stamps)

    for current_number in numbers_drawn:
        print('Drawn: ' + str(current_number))

        if winning_board is not None:
            continue

        for i in range(len(boards)):
            current_board = boards[i]
            current_stamps = stamps[i]

            if current_number in current_board:
                (x, y) = np.where(current_board == current_number)
                current_stamps[x, y] = True
                stamps[i] = current_stamps

                # checking for winning row / col
                for j in range(current_stamps.shape[0]):
                    current_row = current_stamps[j, :]
                    current_col = current_stamps[:, j]

                    if all(current_row) or all(current_col):
                        winning_board = current_board
                        winning_stamps = current_stamps
                        winning_number = current_number

    print('We got a winner! Number drawn: '+str(winning_number))
    inverted_stamps = ~winning_stamps
    unstamped_numbers = winning_board[inverted_stamps]

    score = np.sum(unstamped_numbers) * winning_number
    print('Score: '+str(score))


def get_input():
    assert os.path.exists('input.txt')
    f = open('input.txt', 'r')
    lines = f.readlines()
    f.close()

    count = 0
    numbers_drawn = None
    current_board = None
    boards = []

    # Strips the newline character
    for line in lines:
        if count == 0:
            numbers_drawn = line.split(',')
        else:
            if line.strip() == '':
                boards.append(current_board)
                current_board = []
            else:
                board_line = line.split()
                current_board.append(board_line)

        count += 1

    del current_board
    boards = boards[1:]
    boards = [np.asarray(b, dtype=np.int) for b in boards]
    numbers_drawn = np.asarray(numbers_drawn, dtype=np.int)

    return boards, numbers_drawn


if __name__ == '__main__':
    main()
    print('Done.')
