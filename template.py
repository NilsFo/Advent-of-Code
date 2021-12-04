import os


def main():
    display_input()


def display_input():
    assert os.path.exists('input.txt')
    f = open('input.txt', 'r')
    lines = f.readlines()
    f.close()

    count = 0
    # Strips the newline character
    for line in lines:
        count += 1
        print("Line {}: {}".format(count, line.strip()))


if __name__ == '__main__':
    main()
    print('Done.')
