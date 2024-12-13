import numpy as np
import pandas as pd


class Operator:

    def __init__(self, target_number: int, denominators: [int]):
        super().__init__()
        self.target_number = target_number
        self.denominators = denominators

    def get_calculations(self) -> [str]:
        if len(self.denominators) == 0:
            raise Exception("No denominators provided")

        first_denominator: str = str(self.denominators[0])
        if len(self.denominators) == 1:
            return [first_denominator]

        calculations, results = self._append_number(index=1,
                                                    calculation=first_denominator,
                                                    result=int(first_denominator))
        print(f'Values {self.denominators} have {len(calculations)} permutations of calculations: {calculations}')
        return calculations, results

    def _append_number(self, index, calculation: str, result: int):
        calculation_addition = f'{calculation}+{self.denominators[index]}'
        calculation_multiplication = f'{calculation}*{self.denominators[index]}'
        calculation_cat = f'{calculation}||{self.denominators[index]}'

        # caching the results
        calculation_addition_result = result + self.denominators[index]
        calculation_multiplication_result = result * self.denominators[index]
        calculation_cat_result = int(f'{str(result)}{self.denominators[index]}')

        calculations = [calculation_addition, calculation_multiplication, calculation_cat]
        results = [calculation_addition_result, calculation_multiplication_result, calculation_cat_result]
        if index == len(self.denominators) - 1:
            return calculations, results

        # going deeper in the tree, depending on operation
        appended_calculation_addition, appended_calculation_addition_results = self._append_number(
            index + 1,
            calculation_addition,
            calculation_addition_result
        )
        appended_calculation_multiplication, appended_calculation_multiplication_results = self._append_number(
            index + 1, calculation_multiplication, calculation_multiplication_result
        )
        appended_calculation_cat, appended_calculation_cat_results = self._append_number(
            index + 1, calculation_cat, calculation_cat_result
        )

        # appending results to lists
        appended_calculation_addition.extend(appended_calculation_cat)
        appended_calculation_addition.extend(appended_calculation_multiplication)
        appended_calculation_addition_results.extend(appended_calculation_multiplication_results)
        appended_calculation_addition_results.extend(appended_calculation_cat_results)
        return appended_calculation_addition, appended_calculation_addition_results


def main():
    f = open('input.txt', 'r')
    input = f.read().splitlines()
    f.close()

    operators: [Operator] = []

    for line in input:
        line = line.strip()
        line = line.split(':')

        # target number is on the left
        target_number = int(line[0])

        # possible denominators
        denominators = line[1].split(' ')
        denominators: [int] = [int(d) for d in denominators if len(d) > 0]

        operators.append(Operator(
            target_number=target_number,
            denominators=denominators)
        )

    operation_sums = 0

    # now we evaluate if operations are valid
    for operator in operators:
        calculations, results = operator.get_calculations()
        is_valid = False

        for calculation, result in zip(calculations, results):
            if result == operator.target_number and is_valid is False:
                print(f'[GOTCHA!] {calculation} = {result}')
                operation_sums += operator.target_number
                is_valid = True

    print(f'Operation sums: {operation_sums}')


if __name__ == '__main__':
    main()
