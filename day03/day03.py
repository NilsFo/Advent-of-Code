def main():
    f = open('input.txt')
    lines = f.readlines()
    f.close()

    x = 0
    y = 0

    tree_count = check_slope(lines, 1, 1)
    tree_count = tree_count * check_slope(lines, 3, 1)
    tree_count = tree_count * check_slope(lines, 5, 1)
    tree_count = tree_count * check_slope(lines, 7, 1)
    tree_count = tree_count * check_slope(lines, 1, 2)

    print('Final tree count: ' + str(tree_count))


def check_slope(lines, x: int = 0, y: int = 0):
    tree_count = 0
    start_x = x
    start_y = y

    while y < len(lines):
        line = lines[y].strip()
        c = line[x % len(line)]

        is_tree = c == '#'

        y = y + 1
        x = x + 3

        if is_tree:
            tree_count = tree_count + 1

    print('x=' + str(start_x) + ' y=' + str(start_y) + '. Trees encountered: ' + str(tree_count))
    return tree_count


if __name__ == '__main__':
    main()
