# no imports, wow

class Computer:

    def __init__(self, register_a, register_b, register_c):
        super().__init__()
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c

        self.increment_program_counter = False
        self.program_counter = 0

        self.output_buffer = []

    def format_buffer(self) -> str:
        return ','.join([str(b) for b in self.output_buffer])

    def run_program(self, opcode: int, operand: int):
        self.increment_program_counter = True

        # executing instruction
        if opcode == 0:
            self.adv(operand)
        elif opcode == 1:
            self.bxl(operand)
        elif opcode == 2:
            self.bst(operand)
        elif opcode == 3:
            self.jnz(operand)
        elif opcode == 4:
            self.bxc(operand)
        elif opcode == 5:
            self.out(operand)
        elif opcode == 6:
            self.bdv(operand)
        elif opcode == 7:
            self.cdv(operand)

        if self.increment_program_counter:
            self.program_counter += 2

    def adv(self, operand):
        # The adv instruction (opcode 0) performs division. The numerator is the value in the A register.
        # The denominator is found by raising 2 to the power of the instruction's combo operand.
        # (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
        # The result of the division operation is truncated to an integer and then written to the A register.
        numerator = self.register_a
        denominator = pow(2, self.combo_operand(operand))
        result = numerator // denominator
        self.register_a = result

    def bxl(self, operand):
        # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal
        # operand, then stores the result in register B.
        a = self.register_b
        b = operand
        self.register_b = a ^ b

    def bst(self, operand):
        # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
        # (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        operand = self.combo_operand(operand)
        self.register_b = operand % 8

    def jnz(self, operand):
        # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero,
        # it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps,
        # the instruction pointer is not increased by 2 after this instruction.
        if self.register_a == 0:
            return

        self.program_counter = operand
        self.increment_program_counter = False

    def bxc(self, operand):
        # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
        # then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        a = self.register_b
        b = self.register_c
        result = a ^ b
        self.register_b = result

    def out(self, operand):
        # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
        # (If a program outputs multiple values, they are separated by commas.)
        operand = self.combo_operand(operand)
        result = operand % 8
        self.output_buffer.append(result)

    def bdv(self, operand):
        # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored
        # in the B register. (The numerator is still read from the A register.)
        numerator = self.register_a
        denominator = pow(2, self.combo_operand(operand))
        result = numerator // denominator
        self.register_b = result

    def cdv(self, operand):
        # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in
        # the C register. (The numerator is still read from the A register.)
        numerator = self.register_a
        denominator = pow(2, self.combo_operand(operand))
        result = numerator // denominator
        self.register_c = result

    def combo_operand(self, operand) -> int:
        if operand == 0 or operand == 1 or operand == 2 or operand == 3:
            return operand
        if operand == 4:
            return self.register_a
        if operand == 5:
            return self.register_b
        if operand == 6:
            return self.register_c
        if operand == 7:
            raise ValueError('Illegal combo operand #7!')

    def clear(self):
        self.register_a = 0
        self.register_b = 0
        self.register_c = 0
        self.program_counter = 0
        self.output_buffer = []

    def print_state(self):
        print(f'Register A: {self.register_a}')
        print(f'Register B: {self.register_b}')
        print(f'Register C: {self.register_c}')

        print(f'Output buffer: {self.format_buffer()}')


def main():
    f = open('input.txt', 'r')
    input = f.readlines()
    f.close()

    register_a = None
    register_b = None
    register_c = None
    program: [int] = []

    for line in input:
        line = line.strip()

        # reading register a
        if line.startswith('Register A:'):
            register_a = int(line[11:])
        if line.startswith('Register B:'):
            register_b = int(line[11:])
        if line.startswith('Register C:'):
            register_c = int(line[11:])
        if line.startswith('Program'):
            line = line[9:]

            for byte in line.split(','):
                byte = int(byte.strip())
                program.append(byte)

    ###########################################################
    computer = Computer(
        register_a=register_a,
        register_b=register_b,
        register_c=register_c
    )

    ##### [PART 1]
    print(f'[Part 1] Executing program: {program}')
    run_program(computer=computer,
                program=program,
                verbose=False)

    print(f'[Part 1] Output buffer: {computer.format_buffer()}')

    ##### [PART 2]

    searching = True
    a = 0
    while searching:
        if a % 10000 == 0:
            print(f'Search #{a}')

        computer.clear()
        computer.register_a = a
        run_program(computer=computer, program=program, verbose=False)
        # computer.print_state()

        if computer.output_buffer == program:
            print(f'HIT: {a}')
            searching = False
        a = a + 1

    print('All done.')


def run_program(computer: Computer, program: [int], verbose: bool = True):
    while computer.program_counter < len(program):
        pc = computer.program_counter
        opcode = program[pc]
        operand = program[pc + 1]

        computer.run_program(opcode, operand)

        if verbose:
            print('##########################')
            print(f'PC: {pc}')
            computer.print_state()


if __name__ == '__main__':
    main()
