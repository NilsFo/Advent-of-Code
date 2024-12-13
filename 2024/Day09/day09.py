import numpy as np
import re


def main():
    # first we read and parse the input
    f = open('input.txt')
    input = f.read()
    f.close()

    file_system_length = sum([int(character) for character in input])
    file_system = [-1 for _ in range(file_system_length)]
    file_system = np.asarray(file_system, dtype=int)

    is_file: bool = True
    pointer = 0
    file_id = 0

    for character in input:
        character = int(character)

        for i in range(character):
            if is_file:
                file_system[pointer] = int(file_id)
            pointer += 1

        is_file = not is_file
        if is_file:
            file_id += 1

    print(f'Input file system: {file_system}')
    get_next_free_block(file_system=file_system)

    step_counter = 0
    last_known_pi = -1
    while not is_optimized(file_system=file_system):
        step_counter += 1
        p = float(step_counter) / float(len(file_system)) * 100
        pi = int(p)

        if last_known_pi != pi:
            print(f'Optimizing #{step_counter}/{len(file_system)} [{pi}%]')
            last_known_pi = pi

            f = open('system.txt', 'w')
            f.write(str(list(file_system)))
            f.close()

        file_system = move_last_block(file_system=file_system)
    print('Done.')

    f = open('system.txt', 'w')
    f.write(str(list(file_system)))
    f.close()

    print(f'Optimized file system: {file_system}')

    # getting the checksum
    checksum = 0
    for i, character in enumerate(file_system):
        if character != -1:
            value = i * int(str(character))
            checksum += value
    print(f'Checksum: {checksum}')


def move_last_block(file_system: np.ndarray):
    file_system = np.copy(file_system)
    last_file_block = get_last_file_block(file_system=file_system)
    next_free_block = get_next_free_block(file_system=file_system)

    file_id = file_system[last_file_block]
    file_system[last_file_block] = -1
    file_system[next_free_block] = file_id
    return file_system


def get_last_file_block(file_system: np.ndarray):
    for i in reversed(range(len(file_system))):
        character = file_system[i]
        if character != -1:
            return i
    return None


def get_next_free_block(file_system: np.ndarray):
    for i, character in enumerate(file_system):
        if character == -1:
            return i

    # no more free space :(
    return None


def is_optimized(file_system: np.ndarray) -> bool:
    pattern = re.compile(pattern="^(\\d+)(\\.)+$")
    # system_string = str(list(file_system))[1:-1]
    # system_string = system_string.replace(',', '').replace('\'', '').replace(' ','')
    system_string = ''.join([file_block_to_string(character) for character in file_system])
    fm = pattern.fullmatch(system_string)
    if fm:
        return True
    return False


def file_block_to_string(block: int) -> str:
    if block == -1:
        return '.'
    else:
        return str(block)


def format_system_string(system: np.ndarray):
    pass


if __name__ == '__main__':
    main()

    # too low: 5962471833
    # 6448989155953
