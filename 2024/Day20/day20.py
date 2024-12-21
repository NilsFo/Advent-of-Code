import numpy as np
import cv2

render_scale = 5
cost_cache: np.ndarray[int] = None


class GameState:
    def __init__(self,
                 wall_mask: np.ndarray,
                 bounds_mask: np.ndarray,
                 visited_spaces: np.ndarray,
                 player_position: (int, int),
                 exit_position: (int, int),
                 cost: int
                 ):
        super().__init__()
        self.wall_mask = np.copy(wall_mask)
        self.bounds_mask = np.copy(bounds_mask)
        self.visited_spaces = np.copy(visited_spaces)
        self.player_position = player_position
        self.exit_position = exit_position
        self.cost = cost

        # marking current position as visited
        self.visited_spaces[player_position] = True

    def level_size(self):
        return self.wall_mask.shape[0], self.wall_mask.shape[1]

    def finish_reached(self):
        return self.player_position == self.exit_position

    def render(self, show: bool = True):
        level_size = self.level_size()
        rgb = np.zeros((level_size[0], level_size[1], 3), dtype=np.uint8)

        for i in range(level_size[0]):
            for j in range(level_size[1]):

                # rendering (cheatable) walls
                if self.wall_mask[i, j]:
                    rgb[i, j] = (150, 150, 150)

                # rendering level outline
                if self.bounds_mask[i, j]:
                    rgb[i, j] = (255, 255, 255)

                # rendering player trail
                if self.visited_spaces[i, j]:
                    rgb[i, j] = (120, 0, 0)

                # rendering player
                if i == self.player_position[0] and j == self.player_position[1]:
                    rgb[i, j] = (255, 0, 0)

                # rendering exit
                if i == self.exit_position[0] and j == self.exit_position[1]:
                    rgb[i, j] = (0, 255, 0)

        global render_scale
        new_size = (rgb.shape[0] * render_scale, rgb.shape[1] * render_scale)
        scaled_rgb = cv2.resize(rgb, new_size, interpolation=cv2.INTER_NEAREST)
        if show:
            cv2.imshow('Game', scaled_rgb)
            cv2.waitKey(1)

            cv2.imwrite('frame.png', scaled_rgb)

        return scaled_rgb

    def is_valid_location(self, position: (int, int)):
        in_wall = self.wall_mask[position]
        visited = self.visited_spaces[position]
        in_bounds = self.bounds_mask[position]

        global cost_cache
        cached_cost = cost_cache[position]
        if int(self.cost) >= int(cached_cost):
            # we have been here before. but more efficient.
            return False

        return not in_wall and not visited and not in_bounds

    def update(self):
        # getting the cache
        global cost_cache
        cached_cost = cost_cache[self.player_position]
        if cached_cost > self.cost:
            cost_cache[self.player_position] = self.cost
        else:
            # i am on a field where some other route is more efficient
            # the only solution: unaliving myself
            return []

        # list of possible outcomes
        outcome_states = []

        for direction in other_directions():
            next_position = (
                self.player_position[0] + direction[0],
                self.player_position[1] + direction[1]
            )

            if self.is_valid_location(next_position):
                outcome_states.append(
                    GameState(
                        wall_mask=self.wall_mask,
                        bounds_mask=self.bounds_mask,
                        visited_spaces=self.visited_spaces,
                        player_position=next_position,
                        exit_position=self.exit_position,
                        cost=self.cost + 1
                    )
                )
        return outcome_states


class Cheat:
    def __init__(self,
                 bounds_mask: np.ndarray,
                 visited_spaces: np.ndarray,
                 player_position: (int, int),
                 cost: int
                 ):
        self.bounds_mask = np.copy(bounds_mask)
        self.visited_spaces = np.copy(visited_spaces)
        self.player_position = player_position
        self.cost = cost

        self.visited_spaces[player_position] = True

    def level_size(self):
        return self.bounds_mask.shape

    def is_valid_location(self, position: (int, int)):
        visited = self.visited_spaces[position]
        in_bounds = self.bounds_mask[position]

        # global cost_cache
        # cached_cost = cost_cache[position]
        # if int(self.cost) >= int(cached_cost):
        #    # we have been here before. but more efficient.
        #    return False

        return not visited and not in_bounds

    def update(self):
        new_cheat_states: [Cheat] = []

        for direction in other_directions():
            next_position = (
                self.player_position[0] + direction[0],
                self.player_position[1] + direction[1]
            )

            if self.is_valid_location(next_position):
                new_cheat_states.append(Cheat(
                    bounds_mask=self.bounds_mask,
                    visited_spaces=self.visited_spaces,
                    player_position=next_position,
                    cost=self.cost + 1
                ))

        return new_cheat_states

    def render(self, show: bool = True):
        level_size = self.level_size()
        rgb = np.zeros((level_size[0], level_size[1], 3), dtype=np.uint8)

        for i in range(level_size[0]):
            for j in range(level_size[1]):

                # rendering level outline
                if self.bounds_mask[i, j]:
                    rgb[i, j] = (255, 255, 255)

                # rendering player trail
                if self.visited_spaces[i, j]:
                    rgb[i, j] = (255, 0, 0)

        global render_scale
        new_size = (rgb.shape[0] * render_scale, rgb.shape[1] * render_scale)
        scaled_rgb = cv2.resize(rgb, new_size, interpolation=cv2.INTER_NEAREST)
        if show:
            cv2.imshow('Cheat', scaled_rgb)
            cv2.waitKey(1)

            cv2.imwrite('cheat.png', scaled_rgb)

        return scaled_rgb


def other_directions() -> [(int, int)]:
    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
    ]
    return directions


def main():
    f = open('example.txt')
    input = f.readlines()
    f.close()

    level = []
    for line in input:
        line = line.strip()
        level.append(list(line))

    level = np.array(level, dtype=str)
    level_height, level_width = level.shape

    # wall mask
    wall_mask = np.zeros(level.shape, dtype=bool)
    wall_mask[np.where(level == '#')] = True

    # Creating outer wall
    bounds_mask = np.zeros(level.shape, dtype=bool)
    bounds_mask[0, :] = True
    bounds_mask[-1, :] = True
    bounds_mask[:, 0] = True
    bounds_mask[:, -1] = True

    # Finding the player
    player_position = (
        int(np.where(level == 'S')[0][0]),
        int(np.where(level == 'S')[1][0])
    )

    # Finding the exit
    exit_position = (
        int(np.where(level == 'E')[0][0]),
        int(np.where(level == 'E')[1][0])
    )

    ###########################################################
    del input, level, f, line

    #####################################
    # Running the simulation
    #####################################

    #####################################
    # Baseline path search
    baseline_time, _, baseline_game_state = run_simulation(
        wall_mask=wall_mask,
        bounds_mask=bounds_mask,
        player_position=player_position,
        exit_position=exit_position,
        allow_render_heatmap=False,
    )

    print(f'Baseline time: {baseline_time} picoseconds.')

    #############################
    # cheat mode enabled
    global cost_cache
    baseline_costs = np.copy(cost_cache)
    baseline_costs[exit_position] = baseline_game_state.cost

    print('# CHEAT MODE ENABLED')

    # first we check where the path has been
    visited_spaces = list(np.argwhere(baseline_game_state.visited_spaces))
    visited_spaces = [(int(s[0]), int(s[1])) for s in visited_spaces]

    print(f'Number of spaces visited: {len(visited_spaces)}')
    all_cheat_savings = []
    for i, space in enumerate(visited_spaces):
        print(f'Checking cheats for space #{i + 1}/{len(visited_spaces)}')

        cost = int(baseline_costs[space])
        cheat: Cheat = Cheat(
            bounds_mask=bounds_mask,
            visited_spaces=np.zeros(wall_mask.shape, dtype=bool),
            player_position=space,
            cost=cost
        )

        cheat_savings: [int] = simulate_cheat(initial_cheat=cheat,
                                              iterations=20,
                                              visited_spaces=visited_spaces,
                                              baseline_costs=baseline_costs)
        all_cheat_savings.extend(cheat_savings)

    print('Done.')

    # print(f'Cheat savings: {all_cheat_savings}')
    all_cheat_savings.sort()
    print_unique_counts(numbers=all_cheat_savings)

    saving_threshold = 0
    thresholded_savings = [s for s in all_cheat_savings if s >= saving_threshold]
    print(f'Number of savings >= {saving_threshold}: {len(thresholded_savings)}')


def simulate_cheat(initial_cheat: Cheat,
                   iterations: int,
                   visited_spaces: [(int, int)],
                   baseline_costs: np.ndarray):
    start_position = initial_cheat.player_position
    start_cost = initial_cheat.cost

    cheats = [initial_cheat]
    cheat_results: [Cheat] = []

    for i in range(iterations):
        child_cheats = []
        for cheat in cheats:
            result_cheats = cheat.update()
            child_cheats.extend(result_cheats)
            cheat_results.extend(result_cheats)

        duplicate_cheat_cleaned = []
        for i, cheat_i in enumerate(child_cheats):
            current_cheat = cheat
            current_best_cost = cheat.cost

            for j, cheat_j in enumerate(child_cheats):
                # not checking for the same cheats
                if i == j:
                    continue
                if cheat_j.player_position == current_cheat.player_position:
                    # same cheat has same outcome position
                    if cheat_j.cost < current_best_cost:
                        current_cheat = cheat_j
                        current_best_cost = cheat_j.cost

            duplicate_cheat_cleaned.append(current_cheat)

        cheats = duplicate_cheat_cleaned

    # cheat_result_positions = [c.player_position for c in cheat_results]
    # cheat_result_positions = list(dict.fromkeys(cheat_result_positions))  # removing duplicates
    # print(f'Cheat result positions: {cheat_result_positions}')

    diff_costs = []
    for cheat in cheat_results:
        end_position = cheat.player_position
        end_cost = int(baseline_costs[end_position])
        cheat_cost = int(cheat.cost)

        if end_cost > cheat_cost and end_position in visited_spaces:
            cost_diff = end_cost - start_cost - 2
            diff_costs.append(cost_diff)
            # print(f'Cost difference: {cost_diff}')

    return diff_costs
    # print(f'Diff costs: {diff_costs}')


def render_heat_map(wall_mask: np.ndarray,
                    bounds_mask: np.ndarray):
    global render_scale
    global cost_cache

    cost_values = np.copy(cost_cache)
    cost_values[np.where(cost_values == cost_values.max())] = 0
    max_value = cost_values.max()

    if max_value == 0:
        max_value = 1

    rgb = np.zeros((wall_mask.shape[0], wall_mask.shape[1], 3), dtype=np.uint8)

    for i in range(wall_mask.shape[0]):
        for j in range(wall_mask.shape[1]):
            if bounds_mask[i, j]:
                rgb[i, j] = (210, 210, 210)
            elif wall_mask[i, j]:
                rgb[i, j] = (120, 120, 120)
            else:
                cost = cost_values[i, j]
                cost_percentage = float(cost) / float(max_value)
                rgb[i, j] = (0, 0, int(255 * cost_percentage))

    new_size = (rgb.shape[0] * render_scale, rgb.shape[1] * render_scale)
    scaled_rgb = cv2.resize(rgb, new_size, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Cost', scaled_rgb)
    cv2.waitKey(1)

    cv2.imwrite('cost_cache.png', scaled_rgb)


def print_unique_counts(numbers):
    # Use a dictionary to count occurrences of each unique number
    counts = {}
    for number in numbers:
        counts[number] = counts.get(number, 0) + 1

    # Print each unique number and its count
    for number, count in counts.items():
        print(f"Saving {number} picoseconds: {count}")


def run_simulation(wall_mask: np.ndarray,
                   bounds_mask: np.ndarray,
                   player_position: (int, int),
                   exit_position: (int, int),
                   allow_render: bool = False,
                   allow_render_heatmap: bool = False):
    initial_game_state = GameState(
        wall_mask=wall_mask,
        bounds_mask=bounds_mask,
        player_position=player_position,
        exit_position=exit_position,
        visited_spaces=np.zeros(wall_mask.shape, dtype=bool),
        cost=0
    )
    game_states: [GameState] = [initial_game_state]
    finished_games: [GameState] = []

    global cost_cache
    cache_dtype = np.uint64
    cost_cache = np.full(wall_mask.shape, np.iinfo(cache_dtype).max, dtype=cache_dtype)
    cost_cache[np.where(wall_mask)] = 0
    cost_cache[np.where(bounds_mask)] = 0

    while not len(game_states) == 0:
        new_game_states = []

        for i, game_state in enumerate(game_states):
            child_states = game_state.update()
            new_game_states.extend(child_states)

            if allow_render:
                game_state.render()

        if allow_render_heatmap:
            render_heat_map(wall_mask=wall_mask,
                            bounds_mask=bounds_mask)

        # check if one game_state has reached the end
        for i in reversed(range(len(new_game_states))):
            game_state = new_game_states[i]
            if game_state.finish_reached():
                finished_games.append(game_state)
                del new_game_states[i]

        # updating the list of game states for next iteration
        game_states = new_game_states

    # what is the best tho?
    best_score = np.inf
    best_index = None
    best_game_state = None

    for i, game_state in enumerate(finished_games):
        # print(f'Score of game #{i + 1}: {game_state.cost}')
        best_score = min(best_score, game_state.cost)
        best_index = i

    if best_score == np.inf:
        print('No best game found. The exit cannot be reached.')
    else:
        print(f'Best score is {best_score}')
        best_game_state = finished_games[best_index]
    return best_score, initial_game_state, best_game_state


if __name__ == '__main__':
    main()
