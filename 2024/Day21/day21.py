import sys
from abc import ABC, abstractmethod
from cProfile import label
from typing import Tuple

import numpy as np


class BasePad(ABC):
    def __init__(
            self,
            label: str,
            key_map: np.ndarray
    ):
        self.label = label
        self.key_map = key_map
        self.previous_pad: BasePad = None
        self.check_index1_first: bool = False

        selection_map = np.zeros(key_map.shape, dtype=np.bool)
        selection_map[np.where(key_map == 'A')] = True
        selection = np.where(selection_map == True)
        self._set_selected(selection[0][0], selection[1][0])

        error_map = np.zeros(key_map.shape, dtype=np.bool)
        error_map[np.where(key_map == '')] = True
        error = np.where(error_map == True)
        self.error_tile=(error[0][0], error[1][0])


    def width(self) -> int:
        return self.key_map.shape[0]

    def height(self) -> int:
        return self.key_map.shape[1]

    def _set_selected(self, x, y):
        self.selected_index = (x, y)

    def _out_of_bounds(self, x, y):
        return not (0 <= x < self.width() and 0 <= y < self.height())

    def input_direction(self, direction: str):
        if direction == "<":
            self.input_left()
        if direction == ">":
            self.input_right()
        if direction == "^":
            self.input_up()
        if direction == "v":
            self.input_down()
        if direction == "A":
            self.input_activate()

    def input_up(self):
        x, y = self.selected_index
        new_x = x - 1
        if self._out_of_bounds(new_x, y):
            print("Error: move up would go out of bounds!")
            sys.exit(1)
        self._set_selected(new_x, y)

    def input_down(self):
        x, y = self.selected_index
        new_x = x + 1
        if self._out_of_bounds(new_x, y):
            print("Error: move down would go out of bounds!")
            sys.exit(1)
        self._set_selected(new_x, y)

    def input_left(self):
        x, y = self.selected_index
        new_y = y - 1
        if self._out_of_bounds(x, new_y):
            print("Error: move left would go out of bounds!")
            sys.exit(1)
        self._set_selected(x, new_y)

    def input_right(self):
        x, y = self.selected_index
        new_y = y + 1
        if self._out_of_bounds(x, new_y):
            print("Error: move right would go out of bounds!")
            sys.exit(1)
        self._set_selected(x, new_y)

    def direction_to_key(self, key: str) -> tuple[str, bool]:
        target_position = np.where(self.key_map == key)
        target_position = (target_position[0][0], target_position[1][0])
        current_position = self.selected_index

        if target_position == current_position:
            return 'A', True

        if self.check_index1_first:
            if target_position[1] == current_position[1]:
                if target_position[0] < current_position[0]:
                    return '^', False
                else:
                    return 'v', False
            else:
                if target_position[1] < current_position[1]:
                    return '<', False
                else:
                    return '>', False
        else:
            if target_position[0] == current_position[0]:
                if target_position[1] < current_position[1]:
                    return '<', False
                else:
                    return '>', False
            else:
                if target_position[0] < current_position[0]:
                    return '^', False
                else:
                    return 'v', False

    @abstractmethod
    def input_activate(self):
        pass

    def to_string(self) -> str:
        # ensure 2D
        if self.key_map.ndim != 2:
            raise ValueError("Input array must be 2-dimensional")

        rows, cols = self.key_map.shape

        # compute max width of each column
        col_widths = [
            max(len(self.key_map[r, c]) for r in range(rows))
            for c in range(cols)
        ]

        # helper: horizontal separator
        def sep_line():
            return "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

        lines = []
        lines.append(sep_line())

        # each row
        for r in range(rows):
            row_cells = []
            for c in range(cols):
                val = self.key_map[r, c]
                w = col_widths[c]

                whitespace_char = " "
                if self.selected_index == (r, c):
                    whitespace_char = ":"

                row_cells.append(whitespace_char + val.ljust(w) + whitespace_char)
            lines.append("|" + "|".join(row_cells) + "|")
            lines.append(sep_line())

        return self.label + "\n" + "\n".join(lines)


class KeyPad(BasePad):

    def __init__(
            self,
            label
    ):
        super().__init__(
            label=label,
            key_map=np.array([
                ["7", "8", "9"],
                ["4", "5", "6"],
                ["1", "2", "3"],
                ["", "0", "A"]
            ], dtype=str)
        )

        self.key_history = ''

    def input_activate(self):
        selected_item = self.key_map[self.selected_index]
        self.key_history += selected_item

        if selected_item == 'A':
            # print('Sequence complete: ' + self.key_history)
            self.key_history = ''


class DirectionPad(BasePad):
    def __init__(
            self,
            label: str,
            next_pad: BasePad
    ):
        super().__init__(
            label=label,
            key_map=np.array([
                ["", "^", "A"],
                ["<", "v", ">"]
            ], dtype=str)
        )

        self.next_pad: BasePad = next_pad
        self.next_pad.previous_pad = self

    def input_activate(self):
        s = self.key_map[self.selected_index]
        if s == "<":
            self.next_pad.input_left()
        if s == ">":
            self.next_pad.input_right()
        if s == "^":
            self.next_pad.input_up()
        if s == "v":
            self.next_pad.input_down()
        if s == "A":
            self.next_pad.input_activate()


def main():
    key_pad = KeyPad(
        label='KeyPad'
    )

    robot_pad = DirectionPad(
        label='Robot Pad',
        next_pad=key_pad
    )

    my_pad = DirectionPad(
        label='My Pad',
        next_pad=robot_pad
    )

    # forward_pass(my_pad, "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")
    # forward_pass(my_pad, "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A")
    # forward_pass(my_pad, "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")
    # forward_pass(my_pad, "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A")
    # forward_pass(my_pad, "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")

    input_file_name = "example.txt"

    f = open(input_file_name, 'r')
    lines = f.readlines()
    f.close()

    input_sequences: [str] = []
    for line in lines:
        input_sequences.append(line.strip())

    check_index1_first = False
    key_pad.check_index1_first = True
    robot_pad.check_index1_first = True
    my_pad.check_index1_first = False

    final_score = 0
    for line in input_sequences:
        final_score += input_sequence([key_pad, robot_pad, my_pad], target_sequence=line)

    print(f'Final Score: {final_score}')
    print('Done.')


def input_sequence(pads: [BasePad], target_sequence: str):
    direction_sequence = ""
    first_pad: BasePad = pads[-1]
    last_pad: BasePad = pads[0]

    for char in target_sequence:
        # index 0 prio
        sequence_candidate_1 = enter_code(first_pad, last_pad, char, True)
        direction_sequence += sequence_candidate_1

    print(direction_sequence)

    sequence_score = calculate_score(direction_sequence, target_sequence)
    return sequence_score


def calculate_score(direction_sequence, target_sequence):
    sequence_length = len(direction_sequence)
    sequence_digits = target_sequence[:-1]
    sequence_digits_int = int(sequence_digits)

    sequence_score = sequence_length * sequence_digits_int
    print(f'Sequence "{target_sequence}" score: {sequence_length}*{sequence_digits_int} -> {sequence_score}')
    return sequence_score


def enter_code(first_pad: BasePad, last_pad: BasePad, target: str, verbose: bool = True):
    hit = False
    i = 0
    direction_sequence = ""
    code_entered = False

    while not code_entered:
        target_reached = last_pad.key_map[last_pad.selected_index] == target

        if not target_reached:
            direction, hit = backward_pass(last_pad, target)
        else:
            current_parent: BasePad = last_pad.previous_pad

            while True:
                parent_target_reached = current_parent.key_map[current_parent.selected_index] == "A"

                if parent_target_reached:
                    current_parent = current_parent.previous_pad
                    if current_parent is None:
                        # done, everything aligned
                        direction = "A"
                        code_entered = True
                        break
                else:
                    direction, hit = backward_pass(current_parent, "A")
                    break

        forward_pass(first_pad, direction)

        if verbose:
            print_sequence(last_pad)

        direction_sequence += direction
        # print(direction_sequence)
        i += 1

    return direction_sequence


def backward_pass_local(key_pad: BasePad, target: str):
    hit = False
    backward_history = ''

    while not hit:
        direction, hit = key_pad.direction_to_key(target)
        backward_history += direction
        key_pad.input_direction(direction)

    return backward_history


def backward_pass(key_pad: BasePad, target: str):
    direction, hit = key_pad.direction_to_key(target)

    previous_pad = key_pad.previous_pad
    if previous_pad is not None:
        return backward_pass(previous_pad, direction)

    return direction, hit


def forward_pass(key_pad: BasePad, input_sequence: str):
    for s in input_sequence:
        key_pad.input_direction(s)


def print_sequence(key_pad: BasePad):
    elements: [np.ndarray] = []
    current_pad = key_pad

    elements.append(string_to_array(current_pad.to_string()))
    while current_pad.previous_pad is not None:
        current_pad = current_pad.previous_pad
        elements.append(string_to_array(current_pad.to_string()))

    elements.reverse()

    max_h = max(a.shape[0] for a in elements)

    padded = []
    for a in elements:
        h, w = a.shape
        if h < max_h:
            pad = np.full((max_h - h, w), ' ', dtype=str)
            a = np.vstack([a, pad])
        padded.append(a)

    fused = np.hstack(padded)
    fused = "\n".join("".join(row) for row in fused)
    print(fused)


def string_to_array(s: str):
    lines = s.splitlines()
    maxlen = max(len(line) for line in lines)
    lines = [line.ljust(maxlen) for line in lines]
    return np.array([list(line) for line in lines], dtype=str)


if __name__ == '__main__':
    main()

# too low:
# 191492
