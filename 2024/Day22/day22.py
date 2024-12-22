import numpy as np


class SecretNumber:

    def __init__(self, value: int):
        super().__init__()
        self.value = int(value)

    def __repr__(self):
        return f"SecretNumber({self.value})"

    def mix(self, other_number):
        # To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number.
        # Then, the secret number becomes the result of that operation. (If the secret number is 42 and you
        # were to mix 15 into the secret number, the secret number would become 37.)
        other_number = int(other_number)
        self.value = int(self.value) ^ other_number

    def prune(self):
        # To prune the secret number, calculate the value of the secret number modulo 16777216.
        # Then, the secret number becomes the result of that operation. (If the secret number is 100000000 and
        # you were to prune the secret number, the secret number would become 16113920.)
        self.value = int(self.value) % 16777216


class PriceChart:

    def __init__(self, secret_values: [int], initial_secret_number: int):
        super().__init__()
        self.initial_secret_number = initial_secret_number

        self.prices: [int] = []
        self.changes: [int] = []
        last_known_price = 0

        for i, value in enumerate(secret_values):
            price = int(str(value)[-1])
            self.prices.append(price)

            price_diff = price - last_known_price
            self.changes.append(price_diff)
            last_known_price = price

        # convert to numpy for better debugging
        self.np_values = np.array(secret_values)
        self.np_prices = np.array(self.prices)
        self.np_changes = np.array(self.changes)

    def highest_price(self):
        return max(self.prices)

    def search_price(self, price: int):
        price_array = np.array(self.prices)
        price_indices = np.where(price_array == price)
        price_indices = [int(i) for i in price_indices[0]]
        return price_indices

    def get_change_sequence(self, price_index: int) -> [int, int, int, int]:
        if price_index < 3:
            # index too low
            return None

        change_sequence = [
            self.changes[price_index - 3],
            self.changes[price_index - 2],
            self.changes[price_index - 1],
            self.changes[price_index]
        ]
        return change_sequence

    def find_change_sequence_price(self, change_sequence: [int, int, int, int]) -> (int, int):
        for i in range(len(self.changes) - 3):
            if self.changes[i] == change_sequence[0] and self.changes[i + 1] == change_sequence[1] and self.changes[
                i + 2] == change_sequence[2] and self.changes[i + 3] == change_sequence[3]:
                return self.prices[i + 3], i + 3
        return None, None

    def validate_self(self):
        for price in range(10):
            price_indices = self.search_price(price)
            if len(price_indices) == 0:
                print(f'Price not found: {price}')
                continue

            for i in price_indices:
                price_sequence = self.get_change_sequence(i)
                if price_sequence is not None:
                    best_price = self.find_change_sequence_price(price_sequence)
                    if best_price is not None:
                        print(
                            f'Sequence for price {price} is {price_sequence}: Best price {best_price} (for sanity check)')
                    else:
                        print(f'Sequence not in price changes: {price_sequence}')
                else:
                    print(f'Price has no sequence: {price}')


def main():
    f = open('input.txt', 'r')
    input = f.readlines()
    f.close()
    secret_number_iterations = 2000

    input_numbers: [SecretNumber] = []
    for line in input:
        line = line.strip()
        input_numbers.append(
            SecretNumber(int(line))
        )

    #########################################
    del input, f, line
    final_numbers = []
    price_charts: [PriceChart] = []

    for i, secret_number in enumerate(input_numbers):
        print(f'Processing number {i + 1}/{len(input_numbers)}: {secret_number.value}')
        initial_secret_number = secret_number.value
        secret_numbers: [int] = []
        secret_numbers.append(secret_number.value)

        for j in range(secret_number_iterations):
            p = float(j + 1) / float(secret_number_iterations) * 100
            process(number=secret_number)
            secret_numbers.append(secret_number.value)
            # print(f'Progress: {p:.2f}%: {secret_number.value}')

        price_charts.append(
            PriceChart(secret_values=secret_numbers,
                       initial_secret_number=initial_secret_number)
        )

        print(f'Result: {secret_number.value}')
        final_numbers.append(secret_number.value)

    print(f'Final numbers: {final_numbers}')
    print(f'Sum of all numbers: {sum(final_numbers)}')

    #############################################################
    print('\n###############################\n')
    #############################################################

    # getting possible sequences for every price
    del i, final_numbers, j, p, secret_numbers, input_numbers, secret_number
    price_to_sequence_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

    for price in range(10):
        print(f'Searching all sequences for price {price}/9.')
        for price_chart in price_charts:
            price_indices = price_chart.search_price(price)
            if len(price_indices) == 0:
                # this chart does not sell for the given price
                continue

            # searching price indices for matching sequences
            for i in price_indices:
                price_sequence = price_chart.get_change_sequence(i)
                if price_sequence is not None:
                    known_sequences = price_to_sequence_dict[price]
                    if price_sequence not in known_sequences:
                        price_to_sequence_dict[price].append(price_sequence)

    #############################################################
    print('\n###############################\n')
    #############################################################

    # searching every price sequence in every price chart
    del known_sequences, price, price_chart, price_indices, price_sequence, i

    # cleaning up the sequence dict
    all_sequences: [int, int, int, int] = []
    for i in reversed(range(10)):
        sequences = price_to_sequence_dict[i]
        for sequence in sequences:
            if sequence not in all_sequences:
                all_sequences.append(sequence)

    print(f'Overall, {len(all_sequences)} sequences have been detected.')
    print(str(all_sequences))

    #############################################################
    print('\n###############################\n')
    #############################################################

    # checking every sequence
    best_price = 0
    best_sequence = None

    for i, sequence in enumerate(all_sequences):
        sequence_price = 0
        for chart in price_charts:
            price, _ = chart.find_change_sequence_price(change_sequence=sequence)
            if price is not None:
                sequence_price += price

        print(f'Evaluating prices for sequence {i + 1}/{len(all_sequences)}: {sequence}. Local price: {sequence_price}')

        if sequence_price > best_price:
            best_sequence = sequence
            best_price = sequence_price

    print(f'The best sequence is: {best_sequence}, earning a total of {best_price} bananas.')


def process(number: SecretNumber):
    # STEP 1
    # Calculate the result of multiplying the secret number by 64.
    # Then, mix this result into the secret number. Finally, prune the secret number.
    other_number = number.value * 64
    number.mix(other_number)
    number.prune()

    # STEP 2
    # Calculate the result of dividing the secret number by 32.
    # Round the result down to the nearest integer. Then, mix this result into the secret number.
    other_number = number.value // 32
    number.mix(other_number)

    # STEP 3
    # Finally, prune the secret number.
    # Calculate the result of multiplying the secret number by 2048.
    # Then, mix this result into the secret number. Finally, prune the secret number.
    number.prune()
    other_number = number.value * 2048
    number.mix(other_number)
    number.prune()


if __name__ == '__main__':
    main()
