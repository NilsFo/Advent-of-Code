import numpy as np
import pandas as pd


def main():
    df = pd.read_csv('input.txt', delim_whitespace=True, header=None)
    safe_count = 0

    for row in df.iterrows():
        row = list(row[1])
        row = [int(n) for n in row if not np.isnan(n)]

        is_valid = is_safe(numbers=row, ascending=False) or is_safe(numbers=row, ascending=True)
        print(f'Row: {row}. Passed: {is_valid}')

        if is_valid:
            safe_count += 1

    print(f'Safe: {safe_count}')


def is_safe(numbers: [int], ascending: bool, dampen_mode=False):
    numbers = numbers.copy()
    error_indices = []

    for i in range(len(numbers) - 1):
        current = numbers[i]
        next = numbers[i + 1]

        diff = next - current
        if ascending:
            if diff <= 0:
                error_indices.append(i)
            if diff > 3:
                error_indices.append(i)
        else:
            if diff >= 0:
                error_indices.append(i)
            if diff < -3:
                error_indices.append(i)

    if not dampen_mode and len(error_indices) > 0:
        # adding the final entry just in case
        error_indices.append(len(numbers) - 1)

        for error_index in error_indices:
            damp_numbers = numbers.copy()
            del damp_numbers[error_index]
            damped_safe = is_safe(numbers=damp_numbers, ascending=ascending, dampen_mode=True)
            if damped_safe:
                print(f'DAMP SAFE: {numbers} -> {damp_numbers}')
                return True

    return len(error_indices) == 0


if __name__ == '__main__':
    main()
