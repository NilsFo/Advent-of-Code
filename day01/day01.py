def main():
    f = open('input.txt')
    lines = f.readlines()
    f.close()

    for line1 in lines:
        n1 = int(line1.strip())
        # print(n1)

        for line2 in lines:
            n2 = int(line2.strip())
            # print(n2)

            if n1 == n2:
                continue

            sum = n1 + n2
            mult = n1 * n2
            if sum == 2020:
                print(str(n1) + ' + ' + str(n2) + ' = ' + str(sum) + '. Mult: ' + str(mult))

            for line3 in lines:
                n3 = int(line3.strip())
                if n1 == n3:
                    continue
                if n2 == n3:
                    continue

                sum = n1 + n2 + n3
                mult = n1 * n2 * n3
                if sum == 2020:
                    print(str(n1) + ' + ' + str(n2) + ' + ' + str(n3) + ' = ' + str(sum) + '. Mult: ' + str(mult))


if __name__ == '__main__':
    main()
