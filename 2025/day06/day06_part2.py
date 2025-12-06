import numpy as np
import day06_part1


def main():
    f = 'input.txt'
    f = open(f)
    lines = f.readlines()
    f.close()

    ############################################

    max_length = max([len(l) for l in lines])
    input_sheet = np.full((len(lines), max_length - 1), '')
    operation_indices = []

    for i, line in enumerate(lines):
        line = line.rstrip()

        for j, char in enumerate(line):
            input_sheet[i, j] = char.strip()

        if i == len(lines) - 1:
            pass
            # operations = re.findall(regex_operations, line)

    ############################################
    squid_sheets = split_squid_sheet(input_sheet)

    results = []
    for sheet in squid_sheets:
        shape = sheet.shape

        operation = str(sheet[shape[0] - 1, 0])
        if operation=='':
            operation = str(sheet[shape[0] - 1, 1])

        sheet = sheet[:-1, :]
        results.append(do_squid_math_part2(sheet, operation))

    print(f'Sum of results: {np.sum(results)}.')


def split_squid_sheet(number_sheet):
    sheets = []
    sheet_mask = number_sheet == ''

    split_start_index = 0
    for i in range(number_sheet.shape[1]):
        current_column = sheet_mask[:, i]

        if np.all(current_column):
            current_split = number_sheet[:, split_start_index:i]
            split_start_index = i
            sheets.append(current_split.copy())
    sheets.append(number_sheet[:, split_start_index + 1:])

    return sheets


def do_squid_math_part2(sheet, operation):
    sheet_shape = sheet.shape
    sheet_mask = sheet == ''
    values = []

    for j in range(sheet_shape[1]):
        value = ''

        for i in range(sheet_shape[0]):
            char = sheet[i, j]
            if not sheet_mask[i, j]:
                value = value + str(char)

        if len(value) > 0:
            values.append(value)

    values = [int(v) for v in values]
    return day06_part1.do_squid_math(values, operation)


if __name__ == '__main__':
    main()
