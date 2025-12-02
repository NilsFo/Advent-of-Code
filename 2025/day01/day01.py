import numpy as np


class Vault:

    def __init__(self):
        super().__init__()
        self.value = 50
        self.zeros_reached = 0

    def input(self, direction, value):
        for i in range(value):
            if direction == 'L':
                self.value -= 1

            elif direction == 'R':
                self.value += 1

            self.value %= 100

            if self.value == 0:
                self.zeros_reached += 1


def main():
    input_file_name = "input.txt"

    f = open(input_file_name, 'r')
    lines = f.readlines()
    f.close()

    v = Vault()

    for line in lines:
        line = line.strip()

        direction = line[0]
        value = int(line[1:])

        v.input(direction, value)

    print(v.zeros_reached)


if __name__ == '__main__':
    main()

# too high: 8396