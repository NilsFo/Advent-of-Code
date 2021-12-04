import os

import numpy as np


def main():
    input = get_input()
    assert input is not None

    gamma = []
    lines, bits = input.shape
    for i in range(bits):
        s = sum(input[:, i])
        gamma.append(s > lines / 2)

    assert len(gamma) == bits
    epsilon = ''.join(['0' if b else '1' for b in gamma])
    gamma = ''.join(['1' if b else '0' for b in gamma])
    print('epsilon binary: ' + epsilon)
    print('gamma binary: ' + gamma)

    epsilon = int(epsilon, 2)
    gamma = int(gamma, 2)
    print('epsilon decimal: ' + str(epsilon))
    print('gamma decimal: ' + str(gamma))

    print('mult: ' + str(gamma * epsilon))


def get_input():
    assert os.path.exists('input.txt')
    f = open('input.txt', 'r')
    lines = f.readlines()
    f.close()

    # count = 0
    # # Strips the newline character
    # for line in lines:
    #     count += 1
    #     print("Line {}: {}".format(count, line.strip()))

    return np.asarray([list(l[:-1]) for l in lines], dtype=np.int)


if __name__ == '__main__':
    main()
    print('Done.')
