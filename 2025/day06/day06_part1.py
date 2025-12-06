import re

import numpy as np


def main():
    f = 'example.txt'
    f = open(f)
    lines = f.readlines()
    f.close()

    ############################################

    regex_numbers = re.compile('(\d+)')
    regex_operations = re.compile('(\S+)')
    number_sheet = None
    operations = None

    for i, line in enumerate(lines):
        line = line.strip()

        if i == len(lines) - 1:
            operations = re.findall(regex_operations, line)
        else:
            groups = re.findall(regex_numbers, line)

            if number_sheet is None:
                number_sheet = np.zeros([len(lines) - 1, len(groups)], dtype=np.uint32)

            for j, value in enumerate(groups):
                number_sheet[i, j] = int(value)

    ############################################
    del i, j, line, lines, f, regex_operations, regex_numbers, value, groups

    ####

    results = []
    for i in range(number_sheet.shape[1]):
        values = number_sheet[:, i]
        operation = operations[i]

        result = do_squid_math(values, operation)
        results.append(result)

    print(f'Sum of results: {np.sum(results)}.')


def do_squid_math(values, operation):
    result = int(values[0])

    for v in values[1:]:
        if operation == '+':
            result += int(v)
        elif operation == '*':
            result *= int(v)

    return result


if __name__ == '__main__':
    main()
