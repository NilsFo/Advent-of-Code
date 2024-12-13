import cv2
import numpy as np


class GameBoard:

    def __init__(self, input: [str]):
        super().__init__()

        lines = []
        for line in input:
            line = line.strip()
            lines.append([l for l in line])

        board = np.array(lines, dtype=str)
        self.width = board.shape[0]
        self.height = board.shape[1]

        self.obstacles = []
        self.visited_spaces = []

        for x in range(self.width):
            for y in range(self.height):
                entry = board[x, y]
                if entry == '#':
                    self.obstacles.append((x, y))

                if entry == '^':
                    self.player_position = (x, y)
                    self.player_direction = (-1, 0)
                    self.visited_spaces.append(self.player_position)

    def is_blocked(self, position: (int, int)):
        return position in self.obstacles

    def is_visited(self, position: (int, int)):
        return position in self.visited_spaces

    def is_player(self, position: (int, int)):
        if self.player_position[0] == position[0] and self.player_position[1] == position[1]:
            return True
        return False

    def player_inside(self) -> bool:
        return self.player_position[0] < self.width and self.player_position[1] < self.height

    def tick(self):
        next_position = self.next_player_position()
        if self.is_blocked(next_position):
            self.rotate_player_direction()
        else:
            self.mark_visited(next_position)
            self.player_position = next_position

    def mark_visited(self, position: (int, int)):
        if position[0] >= self.width or position[1] >= self.height:
            return

        if position in self.visited_spaces:
            return
        self.visited_spaces.append(position)

    def next_player_position(self) -> (int, int):
        return (
            self.player_position[0] + self.player_direction[0],
            self.player_position[1] + self.player_direction[1]
        )

    def rotate_player_direction(self):
        if self.player_direction == (-1, 0):  # UP
            self.player_direction = (0, 1)  # RIGHT
        elif self.player_direction == (0, 1):  # RIGHT
            self.player_direction = (1, 0)  # DOWN
        elif self.player_direction == (1, 0):  # DOWN
            self.player_direction = (0, -1)  # LEFT
        elif self.player_direction == (0, -1):  # LEFT
            self.player_direction = (-1, 0)  # UP

    def print_board(self):
        text = ''

        for x in range(self.width):
            for y in range(self.height):
                if self.is_blocked((x, y)):
                    text += '#'
                elif self.is_visited((x, y)):
                    text += 'X'
                elif self.is_player((x, y)):
                    text += '@'
                else:
                    text += '.'
            text += '\n'

        print(text)

    def view_board(self):
        rgb = np.zeros((self.width, self.height, 3), dtype=np.uint8)
        for x in range(self.width):
            for y in range(self.height):
                if self.is_blocked((x, y)):
                    rgb[x, y] = [255, 0, 0]
                elif self.is_visited((x, y)):
                    rgb[x, y] = [0, 255, 0]
                elif self.is_player((x, y)):
                    rgb[x, y] = [0, 0, 255]

        new_size = (rgb.shape[0] * 6, rgb.shape[1] * 6)
        scaled_rgb = cv2.resize(rgb, new_size, interpolation=cv2.INTER_NEAREST)

        cv2.imshow('board', scaled_rgb)
        cv2.waitKey(1)


def main():
    f = open('input.txt', 'r')
    input = f.readlines()
    f.close()

    board: GameBoard = GameBoard(input)
    board.print_board()

    while board.player_inside():
        board.tick()
        board.view_board()
        # board.print_board()

    print(f'Visited spaces: {len(board.visited_spaces)}')


if __name__ == '__main__':
    main()
