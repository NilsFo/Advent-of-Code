import time

import cv2
import numpy as np

render_scale = 10
cost_cache: np.ndarray[int] = None


class GameState:
    def __init__(self,
                 wall_mask: np.ndarray,
                 visited_spaces: np.ndarray,
                 falling_bytes_mask: np.ndarray,
                 player_position: (int, int),
                 exit_position: (int, int),
                 cost: int
                 ):
        super().__init__()
        self.wall_mask = np.copy(wall_mask)
        self.falling_bytes_mask = np.copy(falling_bytes_mask)
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

                # rendering walls
                if self.wall_mask[i, j]:
                    rgb[i, j] = (120, 120, 120)

                # rendering player trail
                if self.visited_spaces[i, j]:
                    rgb[i, j] = (120, 0, 0)

                # rendering player
                if i == self.player_position[0] and j == self.player_position[1]:
                    rgb[i, j] = (255, 0, 0)

                # rendering exit
                if i == self.exit_position[0] and j == self.exit_position[1]:
                    rgb[i, j] = (0, 255, 0)

                # rendering bytes
                if self.falling_bytes_mask[i, j]:
                    rgb[i, j] = (0, 0, 255)

        global render_scale
        new_size = (rgb.shape[0] * render_scale, rgb.shape[1] * render_scale)
        scaled_rgb = cv2.resize(rgb, new_size, interpolation=cv2.INTER_NEAREST)
        if show:
            cv2.imshow('Game', scaled_rgb)
            cv2.waitKey(1)

            cv2.imwrite('frame.png', scaled_rgb)

        return scaled_rgb

    def other_directions(self) -> [(int, int)]:
        directions = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]
        return directions

    def is_valid_location(self, position: (int, int)):
        in_wall = self.wall_mask[position]
        visited = self.visited_spaces[position]
        in_byte = self.falling_bytes_mask[position]

        global cost_cache
        cached_cost = cost_cache[position]
        if int(self.cost) >= int(cached_cost):
            # we have been here before. but more efficient.
            return False

        return not in_wall and not visited and not in_byte

    def update(self):
        # getting the cache
        global cost_cache
        cached_cost = cost_cache[self.player_position]
        if cached_cost > self.cost:
            cost_cache[self.player_position] = self.cost
        else:
            # i am on a field where some route is more efficient
            # the only solution: unsubscribe from life
            return []

        # list of possible outcomes
        outcome_states = []

        for direction in self.other_directions():
            next_position = (
                self.player_position[0] + direction[0],
                self.player_position[1] + direction[1]
            )

            if self.is_valid_location(next_position):
                outcome_states.append(
                    GameState(
                        wall_mask=self.wall_mask,
                        falling_bytes_mask=self.falling_bytes_mask,
                        visited_spaces=self.visited_spaces,
                        player_position=next_position,
                        exit_position=self.exit_position,
                        cost=self.cost + 1
                    )
                )
        return outcome_states


def render_heat_map(wall_mask: np.ndarray,
                    falling_bytes_mask: np.ndarray):
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
            if wall_mask[i, j] or falling_bytes_mask[i, j]:
                rgb[i, j] = (255, 255, 255)
            else:
                cost = cost_values[i, j]
                cost_percentage = float(cost) / float(max_value)
                rgb[i, j] = (0, 0, int(255 * cost_percentage))

    new_size = (rgb.shape[0] * render_scale, rgb.shape[1] * render_scale)
    scaled_rgb = cv2.resize(rgb, new_size, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Cost', scaled_rgb)
    cv2.waitKey(1)

    cv2.imwrite('cost_cache.png', scaled_rgb)


def main():
    f = open('input.txt')
    input = f.readlines()
    f.close()

    falling_bytes = []
    max_byte_position = 0

    for line in input:
        line = line.strip()
        left, right = line.split(',')
        falling_bytes.append((
            int(left),
            int(right)
        ))

        max_byte_position = max(max_byte_position, int(right), int(left))

    # checking if i read example or input, as it is not determined via the input
    map_size_mod = 3
    map_size = (70 + map_size_mod, 70 + map_size_mod)
    if max_byte_position <= 6:
        map_size = (6 + map_size_mod, 6 + map_size_mod)

    del line, input, left, right, max_byte_position
    ########################
    # building board

    wall_mask = np.zeros(map_size, dtype=bool)
    # Creating outer wall
    wall_mask[0, :] = True
    wall_mask[-1, :] = True
    wall_mask[:, 0] = True
    wall_mask[:, -1] = True

    # player position is always top left
    player_position = (1, 1)

    # exit position is always bottom right
    exit_position = (
        map_size[0] - 2,
        map_size[1] - 2
    )

    # running for every bit in a byte and onwards
    bytes_count = 1024
    running = True
    while running:
        best_score, initial_game_state, best_game_state = run_simulation(
            wall_mask=wall_mask,
            bytes_count=bytes_count,
            falling_bytes=falling_bytes,
            player_position=player_position,
            exit_position=exit_position,
            allow_render=False,
            allow_render_heatmap=False
        )

        # check if exit
        if best_score == np.inf:
            byte_placement = falling_bytes[bytes_count-1]
            print(f'Exit cannot be reached anymore at bits: {bytes_count}. Byte placed at: {byte_placement}')
            running = False

            # rendering the final game
            initial_game_state.render(show=True)
            time.sleep(2)

        # increase count for next iteration
        bytes_count += 1


def run_simulation(wall_mask: np.ndarray,
                   bytes_count: int,
                   falling_bytes: [(int, int)],
                   player_position: (int, int),
                   exit_position: (int, int),
                   allow_render: bool = False,
                   allow_render_heatmap: bool = False):
    map_size = wall_mask.shape

    # setting up falling bytes
    bytes_mask = np.zeros(map_size, dtype=bool)
    for i, byte in enumerate(falling_bytes):
        if i < bytes_count:
            bytes_mask[byte[1] + 1, byte[0] + 1] = True

    ######################################################
    # Running the simulation
    initial_game_state: GameState = GameState(
        wall_mask=wall_mask,
        visited_spaces=np.zeros(map_size, dtype=bool),
        falling_bytes_mask=bytes_mask,
        player_position=player_position,
        exit_position=exit_position,
        cost=0
    )
    game_states: [GameState] = [initial_game_state]
    finished_games: [GameState] = []

    global cost_cache
    cache_dtype = np.uint64
    cost_cache = np.full(wall_mask.shape, np.iinfo(cache_dtype).max, dtype=cache_dtype)
    cost_cache[np.where(wall_mask)] = 0

    if allow_render:
        initial_game_state.render()

    # Game Loop
    iterations = 0
    while not len(game_states) == 0:
        new_game_states = []

        for i, game_state in enumerate(game_states):
            child_states = game_state.update()
            new_game_states.extend(child_states)

            if allow_render:
                game_state.render()

        if allow_render_heatmap:
            render_heat_map(wall_mask=wall_mask, falling_bytes_mask=bytes_mask)

        # check if one game_state has reached the end
        for i in reversed(range(len(new_game_states))):
            game_state = new_game_states[i]
            if game_state.finish_reached():
                finished_games.append(game_state)
                del new_game_states[i]

        # updating the list of game states for next iteration
        game_states = new_game_states

        # printing progress
        # iterations += 1
        # print(f'Iteration #{iterations}: {len(new_game_states)} games running. Finished: {len(finished_games)}')

    ##############################################
    # PATHS FOUND
    ##############################################

    # print('###############################')
    # print('## DONE')
    # print('###############################')
    # print(f'Number of finished games: {len(finished_games)}')

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
        print(f'Best score for {bytes_count}/{len(falling_bytes)} is {best_score}')
        best_game_state = finished_games[best_index]
    return best_score, initial_game_state, best_game_state


if __name__ == '__main__':
    main()
