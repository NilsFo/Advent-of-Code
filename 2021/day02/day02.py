import os


def main():
    parse_input()


def parse_input():
    assert os.path.exists('input.txt')
    f = open('input.txt', 'r')
    lines = f.readlines()

    position = 0
    depth = 0
    aim = 0

    # Strips the newline character
    for line in lines:
        direction, magnitude = line.split(' ')
        direction = str(direction)
        magnitude = int(magnitude)
        del line

        if direction == 'forward':
            position = position + magnitude
            depth = depth + aim * magnitude
        if direction == 'down':
            aim = aim + magnitude
        if direction == 'up':
            aim = aim - magnitude

    print('Position: ' + str(position))
    print('Depth: ' + str(depth))
    print('Mult: ' + str(depth * position))


if __name__ == '__main__':
    main()
    print('Done.')
