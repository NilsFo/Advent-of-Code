import re
import time


class CraneGame:
    def __init__(self,
                 prize_x: int, prize_y: int,
                 cost_a: int, cost_b: int,
                 button_a_x: int, button_a_y: int,
                 button_b_x: int, button_b_y: int):
        self.prize_x = int(prize_x)
        self.cost_a = int(cost_a)
        self.button_a_x = int(button_a_x)
        self.button_b_x = int(button_b_x)
        self.prize_y = int(prize_y)
        self.cost_b = int(cost_b)
        self.button_a_y = int(button_a_y)
        self.button_b_y = int(button_b_y)

    def play(self, input_sequence):
        a_button_presses = input_sequence['a']
        b_button_presses = input_sequence['b']

        cost_a = self.cost_a * a_button_presses
        cost_b = self.cost_b * b_button_presses

        claw_position_x = self.button_a_x * a_button_presses + self.button_b_x * b_button_presses
        claw_position_y = self.button_a_y * a_button_presses + self.button_b_y * b_button_presses

        if claw_position_x == self.prize_x and claw_position_y == self.prize_y:
            return cost_a + cost_b
        return None


def main():
    f = open('input.txt')
    input = f.readlines()
    f.close()

    ##################

    crane_games: [CraneGame] = []
    input_sequences = []
    for a in range(100):
        for b in range(100):
            input_sequences.append({'a': a, 'b': b})
    del input_sequences[0]

    for i in range(0, len(input), 4):
        line_a = input[i].strip()
        line_b = input[i + 1].strip()
        line_p = input[i + 2].strip()

        a_x, a_y = re.search(r"X\+(\d+), Y\+(\d+)", line_a).groups()
        b_x, b_y = re.search(r"X\+(\d+), Y\+(\d+)", line_b).groups()
        p_x, p_y = re.search(r"X=(\d+), Y=(\d+)", line_p).groups()

        crane_games.append(CraneGame(
            cost_a=3,
            cost_b=1,
            prize_x=int(p_x) + 10000000000000,
            prize_y=int(p_y) + 10000000000000,
            button_a_x=int(a_x),
            button_b_y=int(b_y),
            button_a_y=int(a_y),
            button_b_x=int(b_x)
        ))

    ##################
    print(f'Number of crane games: {len(crane_games)}')

    ##################
    total_cost = 0
    last_percentage = -1
    button_presses = 10000000000000
    start_time = time.time()

    for a in range(button_presses):
        for b in range(button_presses):
            current_iteration = a * button_presses + b
            total_iterations = button_presses * button_presses

            # PERCENTAGE
            p = int((current_iteration / total_iterations) * 100)
            if p != last_percentage:
                # Calculate ETA
                elapsed_time = time.time() - start_time  # Time elapsed so far
                avg_time_per_iteration = elapsed_time / (current_iteration + 1)  # Average time per iteration
                remaining_iterations = total_iterations - (current_iteration + 1)
                eta_seconds = avg_time_per_iteration * remaining_iterations  # Estimate remaining time in seconds

                # Convert ETA to a date & time
                # eta_datetime = datetime.now() + timedelta(seconds=eta_seconds)

                # print percentage
                last_percentage = p
                print(f'Progress: {p}% - ETA: In {int(eta_seconds)} seconds.')

            # calculating cost
            input_sequence = {'a': a, 'b': b}
            for i, game in enumerate(crane_games):
                cost = game.play(input_sequence=input_sequence)
                if cost is not None:
                    total_cost += cost
                    print(f'Crane game #{i + 1} cost: {cost}')
    print(f'Progress: 100%')

    ##################
    print(f'\n\nTotal cost: {total_cost}')


if __name__ == '__main__':
    main()
