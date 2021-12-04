def main():
    #f = open('example_input.txt')
    f = open('input.txt')
    lines = f.readlines()
    f.close()

    tree_count = 0
    tree_count = check_slope(lines, 1, 1)
    tree_count = tree_count * check_slope(lines, 3, 1)
    tree_count = tree_count * check_slope(lines, 5, 1)
    tree_count = tree_count * check_slope(lines, 7, 1)
    tree_count = tree_count * check_slope(lines, 1, 2)

    print('Final tree count: ' + str(tree_count))


def check_slope(lines, x_step: int = 0, y_step: int = 0):
    tree_count = 0
    x = x_step
    y = y_step

    while y < len(lines):
        line = lines[y].strip()
        c = line[x % len(line)]

        is_tree = c == '#'
        if is_tree:
            tree_count = tree_count + 1

        y = y + y_step
        x = x + x_step

    print('x=' + str(x_step) + ' y=' + str(y_step) + '. Trees encountered: ' + str(tree_count))
    return tree_count


if __name__ == '__main__':
    main()
