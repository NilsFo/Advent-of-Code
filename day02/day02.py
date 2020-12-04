import re


def main():
    f = open('input.txt')
    lines = f.readlines()
    f.close()

    regex = '(\d+)-(\d+) (\w)+: (\w+)'

    between_count = 0
    new_policy_count = 0
    for line1 in lines:
        n1 = str(line1.strip())
        p = re.compile(regex)
        m = p.search(n1)

        low = int(m.group(1))
        high = int(m.group(2))
        c = str(m.group(3))
        pw = str(m.group(4))

        count = pw.count(c)
        in_between = is_between(count, low, high)
        if in_between:
            between_count = between_count + 1

        p1 = pw[low-1]
        p2 = pw[high-1]
        part_finds = 0
        if p1 == c:
            part_finds = part_finds +1
        if p2 == c:
            part_finds = part_finds +1
        if part_finds == 1:
            new_policy_count = new_policy_count +1

    print('Between: ' + str(between_count))
    print('New Policy: ' + str(new_policy_count))


def is_between(x: int, low: int, high: int) -> bool:
    if x < low:
        return False
    if x > high:
        return False
    return True


if __name__ == '__main__':
    main()
