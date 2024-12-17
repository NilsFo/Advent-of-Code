import time

engraving_cache = {0: 1}
splitting_cache = {}
cache_access_engravings: int = 0
cache_access_splits: int = 0


class Stone:

    def __init__(self, engraving: int):
        super().__init__()

        self.engraving: int = int(engraving)

    def blink(self):
        global engraving_cache
        global cache_access_engravings
        global cache_access_splits
        global splitting_cache

        ###########################
        # if zero, set to 1
        ###########################

        if self.engraving == 0:
            self.engraving = 1
            return None

        ##################################
        # split into two
        ##################################

        if self.engraving in splitting_cache.keys():
            digits_left, digits_right = splitting_cache[self.engraving]
            self.engraving = digits_left

            cache_access_splits += 1

            return Stone(digits_right)
        else:
            engraving_digits = str(self.engraving)
            engraving_digit_count = len(engraving_digits)
            if engraving_digit_count % 2 == 0:
                digits_left = engraving_digits[:engraving_digit_count // 2]
                digits_right = engraving_digits[engraving_digit_count // 2:]

                digits_left = int(digits_left)
                digits_right = int(digits_right)

                splitting_cache[self.engraving] = (digits_left, digits_right)

                self.engraving = digits_left
                return Stone(digits_right)

        ########################
        # mult by 2024
        ########################

        new_engraving = None
        if self.engraving in engraving_cache.keys():
            new_engraving = engraving_cache[self.engraving]
            cache_access_engravings += 1

        else:
            new_engraving = self.engraving * 2024
            engraving_cache[self.engraving] = new_engraving

        self.engraving = new_engraving
        return None

    def __str__(self):
        return f'Stone: {self.engraving}'


def main():
    f = open('input.txt', 'r')
    input = f.read()
    f.close()

    ######################
    # READING ENGRAVINGS

    stone_engravings = input.split(' ')
    # stones: [Stone] = []
    # for engraving in stone_engravings:
    #    engraving = int(engraving.strip())
    #    stones.append(Stone(engraving))
    stone_engravings = [int(e) for e in stone_engravings]

    #######################
    # BLINKING
    global cache_access_engravings
    global cache_access_splits

    blinks = 75
    stone_count = 0
    for s,engraving in enumerate(stone_engravings):
        cache_access_engravings = 0
        cache_access_splits = 0

        stones:[Stone] = [Stone(engraving)]

        cache_access_engravings = 0
        for b in range(blinks):
            start_time = time.time()

            for i in reversed(range(len(stones))):
                new_stone = stones[i].blink()
                if new_stone is not None:
                    stones.append(new_stone)

            end_time = time.time()
            duration = int(end_time - start_time)
            print(f'\n########################\n### BLINK {b + 1}')
            print(f'Stone #{s + 1} done.')
            #print(f'Number of stones after {b + 1} blinks: {len(stones)}.')
            #print(f'Engraving cache accessed: {cache_access_engravings}. Splits: {cache_access_splits}')
            print(f'Time taken: {duration} seconds.')

        stone_count += len(stones)

    print('\n#######################')
    print(f'Final Stone count: {stone_count}')

if __name__ == '__main__':
    main()
