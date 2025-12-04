import numpy as np


def main():
    f = 'input.txt'
    f = open(f)
    lines = f.readlines()
    f.close()

    banks = []
    for l in lines:
        l = l.strip()
        banks.append([int(i) for i in l])

    largest_joltages = []

    for bank in banks:
        joltage = calculate_joltage_day2(bank)
        largest_joltages.append(joltage)

        print(f'Largest joltage for "{bank}" is: {joltage}')

    jolt_sum = np.sum(largest_joltages)
    print(f'Total joltage output: {int(jolt_sum)}')


def calculate_joltage_day1(bank: list[int]):
    # finding first largest breaker
    max_breaker_l, breaker_index_l = highest_index(bank[:-1])

    # finding the largest breaker to the right side of that
    right_side_breaker = bank[breaker_index_l + 1:]
    max_breaker_r, breaker_index_r = highest_index(right_side_breaker)

    # calculating biggest joltage
    return max_breaker_l * 10 + max_breaker_r


def calculate_joltage_day2(bank: list[int]):
    current_bank = bank.copy()
    breaker_sequence = []
    remaining_numbers = 12
    skipped_numbers = 0

    for i in range(12):
        sub_bank = bank.copy()
        if i < 12:
            sub_bank = bank[skipped_numbers:len(bank)-remaining_numbers+1]

        max_breaker, breaker_index = highest_index(sub_bank)
        remaining_numbers -= 1
        skipped_numbers += breaker_index+1

        current_bank = current_bank[breaker_index + 1:]
        breaker_sequence.append(max_breaker)
        # print(i)

    breakers = ''
    for b in breaker_sequence:
        breakers = breakers + str(b)

    return int(breakers)


def append_str(a, b):
    return str(a) + str(b)


def highest_index(bank: list[int]):
    bank = np.array(bank, dtype=np.int8)
    max_breaker = int(np.max(bank))
    breaker_where = np.where(bank == int(max_breaker))

    if type(breaker_where) == tuple:
        breaker_where = breaker_where[0]

    return max_breaker, int(breaker_where[0])


if __name__ == '__main__':
    main()
