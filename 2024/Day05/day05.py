import random
import re

import numpy as np
import pandas as pd


class Rule:

    def __init__(self, before: int, after: int):
        super().__init__()

        self.before = before
        self.after = after

    def has(self, page: int):
        return self.before == page or self.after == page

    def check_pages(self, current_page: int, other_page: int, before_state: bool):
        if not self.has(current_page):
            return True
        if not self.has(other_page):
            return True

        if not before_state:
            return self.before == current_page and self.after == other_page
        else:
            return self.after == current_page and self.before == other_page


rules: [Rule] = []
updates = []


def main():
    f = open('input.txt')
    input = f.readlines()
    f.close()

    global rules
    global updates

    read_mode_rules = True
    for line in input:
        line = line.strip()

        if line == '':
            read_mode_rules = False
            continue

        # print(f'{read_mode_rules} -> {line}')
        if read_mode_rules:
            pattern = re.compile('(\\d+)\\|(\\d+)')

            for match in pattern.finditer(line):
                l = int(match.group(1))
                r = int(match.group(2))
                rules.append(Rule(l, r))
                del l, r
        else:
            splits = line.split(',')
            updates.append([int(s) for s in splits])
            del splits

    ##################################################
    del line, read_mode_rules, f
    ##################################################

    middle_sum = 0
    incorrect_updates: [] = []
    correct_updates: [] = []
    for update in updates:
        correct = check_update(update)

        if correct:
            middle = update[len(update) // 2]
            # print(f'Middle of {update} is: {middle}')
            middle_sum += middle
            correct_updates.append(update)
        else:
            incorrect_updates.append(update)

    print(f'sum of correct updates sum: {middle_sum}')
    print(f'Incorrect updates: {len(correct_updates)}/{len(updates)}')

    middle_sum = 0
    for i in range(len(incorrect_updates)):
        current_incorrect_update = incorrect_updates[i]
        print(f'Fixing update #{i + 1}/{len(incorrect_updates)}: {current_incorrect_update}')

        # corrected = False
        # while not corrected:
        #    # bogo sort, heck yea! >:)
        #    random.shuffle(current_incorrect_update)
        #    corrected = check_update(current_incorrect_update)
        #    print(f'\r{current_incorrect_update}')

        sorted_update = sort_update(current_incorrect_update)
        middle = sorted_update[len(sorted_update) // 2]
        middle_sum += middle

    print(f'sum of corrected updates sum: {middle_sum}')


def sort_update(update):
    sorted_update = []
    update = update.copy()

    while len(update) > 0:
        lowest = get_lowest(update)
        lowest_index = update.index(lowest)
        del update[lowest_index]
        sorted_update.append(lowest)

    return sorted_update


def get_lowest(update) -> int:
    for i in range(len(update)):
        current_page = update[i]
        all_ok = True

        for j in range(len(update)):
            if i == j or not all_ok:
                continue

            other_page = update[j]
            rule_ok = check_rule(page=current_page,
                                 other_page=other_page,
                                 before=False)
            all_ok = all_ok and rule_ok

        if all_ok:
            return current_page


def check_update(update):
    correct = True
    for i, page in enumerate(update):
        correct = correct and is_correct_page(i, update)

    return correct


def is_correct_page(index: int, update: [int]):
    # print(f'{index}: {update}')
    current_page = update[index]
    is_valid = True

    for i, other_page in enumerate(update):
        if i == index:
            continue

        before = i < index
        passed_rule = check_rule(page=current_page, other_page=other_page, before=before)
        # print(f'Comparing [{current_page} to {other_page}] in {update} -> {passed_rule}')

        is_valid = is_valid and passed_rule

    return is_valid


def check_rule(page: int, other_page: int, before: bool):
    global rules
    is_valid = True

    for rule in rules:
        r: Rule = rule
        if r.has(page) and r.has(other_page):
            is_valid = is_valid and r.check_pages(current_page=page,
                                                  other_page=other_page,
                                                  before_state=before)

    return is_valid


if __name__ == '__main__':
    main()
