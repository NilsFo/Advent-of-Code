import os
import re

import cv2
import numpy as np


class Robot:

    def __init__(self, position: (int, int), velocity: (int, int)):
        super().__init__()
        self.position = position
        self.velocity = velocity

    def __str__(self):
        return f'Robot. Position: {self.position}, Velocity: {self.velocity}'

    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

    def move(self, board_size: (int, int)):
        new_position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1]
        )

        # teleporting / wrapping around
        new_position = (
            new_position[0] % board_size[0],
            new_position[1] % board_size[1]
        )

        self.position = new_position


def main():
    f = open('input.txt', 'r')
    input = f.readlines()
    f.close()

    robots: [Robot] = []
    board_size = (
        103,  # 103
        101  # 101
    )

    for line in input:
        line = line.strip()
        py, px, vy, vx = re.search(r"p=(-*\d+),(-*\d+) v=(-*\d+),(-*\d+)", line).groups()
        robots.append(
            Robot(
                position=(int(px), int(py)),
                velocity=(int(vx), int(vy))
            )
        )

    print(f'Number of robots: {len(robots)}')
    print('##########################')
    print_board(robots=robots, board_size=board_size)
    view_board(robots=robots, board_size=board_size)

    # prepping output dir
    out_dir_base = 'output'

    #####################
    # MOVING ROBOTS
    for i in range(10000):
        # moving robots for 100 seconds
        for robot in robots:
            robot.move(board_size)

        print(f'Movement {i + 1}')

        folder_id = str(i // 500)
        out_dir = f'{out_dir_base}{os.sep}{folder_id}'
        os.makedirs(out_dir, exist_ok=True)
        out_name = f'{out_dir}{os.sep}robots{i}.png'

        if not os.path.exists(out_name):
            rgb_image = view_board(robots=robots, board_size=board_size)
            cv2.imwrite(out_name, rgb_image)

    print('Moving done.')

    ###############
    # Quartering
    ###############

    center_x = board_size[0] // 2
    center_y = board_size[1] // 2
    quadrants = {
        "Q1": [],  # Top-right
        "Q2": [],  # Top-left
        "Q3": [],  # Bottom-left
        "Q4": []  # Bottom-right
    }
    for robot in robots:
        x = robot.x()
        y = robot.y()
        if x > center_x and y > center_y:
            quadrants["Q1"].append(robot)
        elif x < center_x and y > center_y:
            quadrants["Q2"].append(robot)
        elif x < center_x and y < center_y:
            quadrants["Q3"].append(robot)
        elif x > center_x and y < center_y:
            quadrants["Q4"].append(robot)

    # printing quadrants
    safety_factor = 1
    for quadrant, robots in quadrants.items():
        print(f'#### {quadrant}: {len(robots)} #########################')
        print_board(robots=robots, board_size=board_size)
        safety_factor *= len(robots)

    print(f'Safe factor: {safety_factor}')


def print_board(robots: [Robot], board_size: (int, int)):
    for i in range(board_size[0]):
        for j in range(board_size[1]):
            character = '.'

            # checking for robots at position
            robots_at_position = find_robots(robots=robots, position=(i, j))
            if len(robots_at_position) > 0:
                character = str(len(robots_at_position))

            print(character, end='')
        print('\n', end='')


def view_board(robots: [Robot], board_size: (int, int), scale: int = 8) -> np.ndarray:
    rgb = np.zeros((board_size[0], board_size[1], 3), dtype=np.uint8)
    for i in range(board_size[0]):
        for j in range(board_size[1]):
            robots_at_position = find_robots(robots=robots, position=(i, j))
            if len(robots_at_position) > 0:
                rgb[i, j] = [min(255, 100 + len(robots_at_position) * 50), 0, 0]
    # rgb[0, 0] = [255, 255, 255]

    new_size = (rgb.shape[0] * scale, rgb.shape[1] * scale)
    scaled_rgb = cv2.resize(rgb, new_size, interpolation=cv2.INTER_NEAREST)

    cv2.imshow('board', scaled_rgb)
    cv2.waitKey(1)

    return scaled_rgb


def find_robots(robots: [Robot], position: (int, int)) -> [Robot]:
    found_robots = []
    for robot in robots:
        if robot.x() == position[0] and robot.y() == position[1]:
            found_robots.append(robot)
    return found_robots


if __name__ == '__main__':
    # easter egg at time step 6531
    main()
