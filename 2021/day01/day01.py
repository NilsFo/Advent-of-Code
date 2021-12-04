import math
import os


def main():
    parse_input()


def parse_input():
    assert os.path.exists('input.txt')
    f = open('input.txt', 'r')
    lines = f.readlines()
    f.close()

    count = 0
    last_entry = math.nan
    current_entry = math.nan

    decreased_count = 0
    increased_count = 0

    # Strips the newline character
    for line in lines:
        count += 1

        current_entry = int(line.strip())
        del line

        if count > 1:
            if current_entry < last_entry:
                decreased_count = decreased_count + 1
            if current_entry > last_entry:
                increased_count = increased_count + 1

        last_entry = current_entry

    print('Decreased: ' + str(decreased_count))
    print('Increased: ' + str(increased_count))


if __name__ == '__main__':
    main()
    print('Done.')
