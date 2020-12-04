def main():
    #f = open('example_input.txt')
    f = open('input.txt')
    lines = f.readlines()
    f.close()

    passports = []
    current_pp = {}
    for line in lines:
        line = line.strip()

        if len(line) == 0:
            passports.append(current_pp)
            current_pp = {}
            continue

        entries = line.split(' ')
        for entry in entries:
            entry = entry.split(':')
            current_pp[entry[0]] = entry[1]

    passports.append(current_pp)
    print('Passports found: ' + str(len(passports)))

    valid_count = 0
    for passport in passports:
        if is_valid(passport):
            valid_count = valid_count + 1

    print('Valid passports: ' + str(valid_count))


def is_valid(passport: dict) -> bool:
    required_entries = [
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid'
        # 'cid' Surely, nobody would mind... >.>
    ]

    for entry in required_entries:
        if entry not in passport.keys():
            return False

    return True


if __name__ == '__main__':
    main()
