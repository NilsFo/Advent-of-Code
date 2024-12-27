import re
import time
from asyncore import write

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

wires_circuit = {}
wire_as_output = {}


def parse_file(file_path):
    key_value_dict = {}
    assignments = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Parse key-value pairs using regex
        key_value_match = re.match(r"^(\w+):\s*(\d+)$", line)
        if key_value_match:
            key = key_value_match.group(1)
            value = int(key_value_match.group(2))
            key_value_dict[key] = value
            continue

        # Parse assignment lines using regex
        assignment_match = re.match(r"^(\w+)\s+(AND|OR|XOR)\s+(\w+)\s+->\s+(\w+)$", line)
        if assignment_match:
            input1 = assignment_match.group(1)
            operation = assignment_match.group(2).upper()
            input2 = assignment_match.group(3)
            output = assignment_match.group(4)
            assignments.append((input1, input2, operation, output))

    return key_value_dict, assignments


class Connection:
    def __init__(self, input_1: str, input_2: str, operation: str, output: str):
        self.input_1 = input_1
        self.input_2 = input_2
        self.output = output
        self.operation = operation

    def __str__(self):
        return f'CONN({self.input_1} {self.operation} {self.input_2} -> {self.output})'

    def calculate(self):
        global wires_circuit
        global wire_as_output

        input_1_value = None
        input_2_value = None

        if self.input_1 not in wires_circuit.keys():
            wire_as_output[self.input_1][0].calculate()

        if self.input_2 not in wires_circuit.keys():
            wire_as_output[self.input_2][0].calculate()

        input_1_value = wires_circuit[self.input_1]
        input_2_value = wires_circuit[self.input_2]
        input_1_value = bool(input_1_value)
        input_2_value = bool(input_2_value)

        operation_result = None
        ## applying operation
        if self.operation == 'AND':
            operation_result = input_1_value & input_2_value
        elif self.operation == 'OR':
            operation_result = input_1_value | input_2_value
        elif self.operation == 'XOR':
            operation_result = input_1_value ^ input_2_value
        else:
            raise ValueError(f'Operation {self.operation} not supported')

        wires_circuit[self.output] = operation_result


def main():
    defaults, connections = parse_file(file_path='input.txt')

    ###################################################################

    global wires_circuit
    global wire_as_output
    wires_circuit = {}
    wire_as_output = {}

    all_wire_names = []
    for k in defaults.keys():
        wires_circuit[k] = defaults[k] == 1

        if k not in all_wire_names:
            all_wire_names.append(k)

    #############
    del k, defaults
    #############

    all_connections = []
    for connection in connections:
        input_1, input_2, operation, output = connection
        connection = Connection(
            input_1=input_1,
            input_2=input_2,
            operation=operation,
            output=output
        )
        all_connections.append(connection)

        if output not in wire_as_output:
            wire_as_output[output] = []
        wire_as_output[output].append(connection)

        for k in [input_1, input_2, output]:
            if k not in all_wire_names:
                all_wire_names.append(k)

    #############################################
    ## PART 1
    del connections, input_1, input_2, output, k, operation, connection
    all_wire_names.sort()
    #############################################
    for i in tqdm(range(len(all_connections))):
        connection = all_connections[i]
        connection.calculate()

    time.sleep(1)
    print('Done.')

    #############################################
    del i
    #############

    result_bits = []
    for i, wire_name in enumerate(all_wire_names):
        w = bool(wires_circuit[wire_name])
        bit = '0'
        if w:
            bit='1'
        print(f'{wire_name}: {bit}')

        if wire_name.startswith('z'):
            result_bits.append(w)

    result_bits.reverse()
    print(f'Resulting bit length: {len(result_bits)}')
    bit_string = ''.join('1' if b else '0' for b in result_bits)
    result = int(bit_string, 2)
    print(f'Converting "{bit_string}" -> {result}.')


if __name__ == '__main__':
    main()
