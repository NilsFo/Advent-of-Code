import sys
import time

import cv2
import numpy as np

cost_cache: np.ndarray[int] = None
render_scale: int = 5


class GameState:

    def __init__(self,
                 wall_mask: np.ndarray,
                 visited_spaces: np.ndarray,
                 player_position: (int, int),
                 player_direction: (int, int),
                 exit_position: (int, int),
                 allow_rotation: bool,
                 cost: int
                 ):
        super().__init__()
        self.wall_mask = np.copy(wall_mask)
        self.visited_spaces = np.copy(visited_spaces)
        self.player_position = player_position
        self.player_direction = player_direction
        self.exit_position = exit_position
        self.cost = cost

        # movement restrictions
        self.allow_rotation = allow_rotation

        # marking current position as visited
        self.visited_spaces[player_position] = True

    def level_size(self):
        return self.wall_mask.shape[0], self.wall_mask.shape[1]

    def other_directions(self) -> [(int, int)]:
        directions = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]
        directions.remove(self.player_direction)
        return directions

    def is_valid_location(self, position: (int, int)):
        global cost_cache
        cached_cost = cost_cache[position]
        # if self.cost > cached_cost:
        #     # we have been here before. but more efficient.
        #     return False

        # cost_diff = abs(cached_cost - self.cost)
        # if cost_diff < 50000:
        #    # we have been here before. but more efficient.
        #    return False

        return not self.wall_mask[position] and not self.visited_spaces[position]

    def finish_reached(self):
        return self.player_position == self.exit_position

    def update(self):
        # getting the cache
        global cost_cache
        cached_cost = cost_cache[self.player_position]
        if cached_cost > self.cost:
            cost_cache[self.player_position] = self.cost

        # list of possible outcomes
        outcome_states = []

        next_position = (
            self.player_position[0] + self.player_direction[0],
            self.player_position[1] + self.player_direction[1]
        )

        # would we move into a wall or a space where we have already been?
        if self.is_valid_location(next_position):
            outcome_states.append(
                GameState(
                    wall_mask=self.wall_mask,
                    visited_spaces=self.visited_spaces,
                    player_position=next_position,
                    player_direction=self.player_direction,
                    exit_position=self.exit_position,
                    allow_rotation=True,
                    cost=self.cost + 1
                )
            )

        # adding rotations to the list of possible moves
        other_directions = self.other_directions()
        for direction in other_directions:
            next_position = (
                self.player_position[0] + direction[0],
                self.player_position[1] + direction[1]
            )
            if self.is_valid_location(next_position) and self.allow_rotation:
                outcome_states.append(
                    GameState(
                        wall_mask=self.wall_mask,
                        visited_spaces=self.visited_spaces,
                        player_position=self.player_position,
                        player_direction=direction,
                        exit_position=self.exit_position,
                        allow_rotation=False,
                        cost=self.cost + 1000
                    )
                )

        # returning the new states
        return outcome_states

    def render(self, show: bool = True):
        level_size = self.level_size()
        rgb = np.zeros((level_size[0], level_size[1], 3), dtype=np.uint8)

        for i in range(level_size[0]):
            for j in range(level_size[1]):

                # rendering walls
                if self.wall_mask[i, j]:
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

            cv2.imwrite('game.png', scaled_rgb)

        return scaled_rgb


def render_heat_map(wall_mask: np.ndarray):
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
            if wall_mask[i, j]:
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

    # player position
    player_position = np.where(level == 'S')
    player_position = (
        int(player_position[0][0]),
        int(player_position[1][0])
    )

    # exit position
    exit_position = np.where(level == 'E')
    exit_position = (
        int(exit_position[0][0]),
        int(exit_position[1][0])
    )

    # visited spaces
    visited_spaces = np.zeros(level.shape, dtype=bool)
    visited_spaces[player_position] = True

    # initial direction
    player_direction: (int, int) = (0, 1)

    global cost_cache
    cache_dtype = np.uint64
    cost_cache = np.full(wall_mask.shape, np.iinfo(cache_dtype).max, dtype=cache_dtype)
    cost_cache[np.where(wall_mask)] = 0

    #############################
    # SETTING UP GAME
    #############################
    initial_game_state = GameState(
        wall_mask=wall_mask,
        visited_spaces=visited_spaces,
        player_position=player_position,
        player_direction=player_direction,
        exit_position=exit_position,
        allow_rotation=True,
        cost=0
    )
    initial_game_state.render()

    ##########################
    game_states = [initial_game_state]
    finished_games = []
    render_enabled = False
    iterations = 0

    while len(game_states) > 0:
        new_game_states = []
        for game_state in game_states:
            if render_enabled:
                game_state.render()
                # sleep, so i can watch the renders
                time.sleep(0.025)

            child_states = game_state.update()
            new_game_states.extend(child_states)

        # check if one game_state has reached the end
        for i in reversed(range(len(new_game_states))):
            game_state = new_game_states[i]
            if game_state.finish_reached():
                finished_games.append(game_state)
                del new_game_states[i]

        # updating the list of game states for next iteration
        game_states = new_game_states

        # rendering the current cost cache
        render_heat_map(wall_mask=wall_mask)

        # printing progress
        iterations += 1
        print(f'Iteration #{iterations}: {len(new_game_states)} games running. Finished: {len(finished_games)}')

    ##############################################
    # PATHS FOUND
    ##############################################

    print('###############################')
    print('## DONE')
    print('###############################')

    print(f'Number of finished games: {len(finished_games)}')

    # what is the best tho?
    best_score = np.inf
    best_index = None
    best_seats_mask = np.zeros(wall_mask.shape, dtype=bool)

    for i, game_state in enumerate(finished_games):
        print(f'Score of game #{i + 1}: {game_state.cost}')
        best_score = min(best_score, game_state.cost)
        best_index = i

        cost_cache[game_state.player_position] = best_score

    for i, game_state in enumerate(finished_games):
        if game_state.cost == best_score:
            best_seats_mask[np.where(game_state.visited_spaces)] = True

    print(f'Best score is {best_score}')
    print(f'Best seats count: {len(np.where(best_seats_mask)[0])}')
    best_game_state = finished_games[best_index]
    best_game_state.render()
    render_heat_map(wall_mask=wall_mask)
    time.sleep(2)


if __name__ == '__main__':
    main()
