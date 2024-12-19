import cv2
import numpy as np


class Barrel:

    def __init__(self, position: (int, int)):
        super().__init__()
        self.position = position

    def gps_coordinates(self) -> int:
        return self.position[0] * 100 + self.position[1]


class Game:

    def __init__(self,
                 wall_mask: np.ndarray,
                 player_position: (int, int),
                 barrels: [Barrel]):
        super().__init__()
        self.wall_mask = wall_mask
        self.player_position = player_position
        self.barrels = barrels

    def level_size(self):
        return self.wall_mask.shape[0], self.wall_mask.shape[1]

    def render(self, scale: int = 20, show: bool = True) -> np.ndarray:
        level_size = self.level_size()
        rgb = np.zeros((level_size[0], level_size[1], 3), dtype=np.uint8)

        for i in range(level_size[0]):
            for j in range(level_size[1]):

                # rendering walls
                if self.wall_mask[i, j]:
                    rgb[i, j] = (255, 0, 0)

                # rendering barrels
                if self.is_barrel((i, j)):
                    rgb[i, j] = (0, 0, 255)

                # rendering player
                if i == self.player_position[0] and j == self.player_position[1]:
                    rgb[i, j] = (0, 255, 0)

        new_size = (rgb.shape[0] * scale, rgb.shape[1] * scale)
        scaled_rgb = cv2.resize(rgb, new_size, interpolation=cv2.INTER_NEAREST)
        cv2.imwrite('frame.png', scaled_rgb)

        if show:
            cv2.imshow('Game', scaled_rgb)
            cv2.waitKey(1)

        return scaled_rgb

    def is_barrel(self, position):
        return position in [b.position for b in self.barrels]

    def get_barrel_at(self, position) -> Barrel:
        for barrel in self.barrels:
            if barrel.position[0] == position[0] and barrel.position[1] == position[1]:
                return barrel
        return None

    def step(self, direction):
        next_position = (
            self.player_position[0] + direction[0],
            self.player_position[1] + direction[1]
        )

        if self.wall_mask[next_position[0], next_position[1]]:
            # we are blocked by a wall. not moving
            return

        # checking for barrel collision
        if self.is_barrel(next_position):
            barrel_pushable = self.check_barrel_push(position=next_position,
                                                     direction=direction,
                                                     barrel_stack=[])
            if barrel_pushable:
                self.player_position = next_position
                return
            else:
                return

        self.player_position = next_position

    def check_barrel_push(self,
                          position: (int, int),
                          direction: (int, int),
                          barrel_stack: [Barrel]
                          ) -> bool:
        current_barrel = self.get_barrel_at(position)
        next_position = (
            current_barrel.position[0] + direction[0],
            current_barrel.position[1] + direction[1]
        )

        if self.wall_mask[next_position[0], next_position[1]]:
            # barrel_stack is blocked by wall
            return False

        if self.is_barrel(next_position):
            child_barrel_ok = self.check_barrel_push(position=next_position,
                                                     direction=direction,
                                                     barrel_stack=barrel_stack)
            if not child_barrel_ok:
                return False

        # moving the barrel
        current_barrel.position = next_position
        return True

    def barrel_gps_coordinates(self) -> int:
        sum = 0
        for barrel in self.barrels:
            sum += barrel.gps_coordinates()
        return sum


def main():
    f = open('input.txt')
    input = f.readlines()
    f.close()

    input_sequence = ''
    input_map = []

    for line in input:
        line = line.strip()
        if len(line) > 0:
            if line.startswith('#'):
                # map line
                input_map.append(list(line))
            else:
                # input line
                input_sequence = line

    print(f'Input sequence length: {len(input_sequence)}')
    del f, line, input

    ################################
    # parsing level layout
    ################################
    input_map = np.array(input_map, dtype=str)
    barrels = []

    # extracting walls
    wall_mask = np.zeros(input_map.shape, dtype=bool)
    wall_mask[np.where(input_map == '#')] = True

    # extracting player position
    player_position = np.where(input_map == '@')
    player_position = (
        int(player_position[0][0]),
        int(player_position[1][0])
    )

    # extracting barrels
    barrel_positions = np.where(input_map == 'O')
    for a, b in zip(barrel_positions[0], barrel_positions[1]):
        barrels.append(Barrel((a, b)))

    # setting up the game state
    game: Game = Game(wall_mask=wall_mask,
                      player_position=player_position,
                      barrels=barrels)

    scale = 30
    initial_render = game.render(scale=scale, show=False)

    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec (use 'mp4v' for MP4 if needed)
    out = cv2.VideoWriter('robot_video.avi', fourcc, fps, (initial_render.shape[0], initial_render.shape[1]))

    for i, input in enumerate(input_sequence):
        print(f'Processing input #{i + 1}/{len(input_sequence)}: {input}')
        direction = input_to_direction(input)

        game.step(direction)
        rgb_frame = game.render(show=False, scale=scale)
        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        out.write(bgr_frame)

    out.release()
    cv2.destroyAllWindows()

    print('Done.')
    print(f'Barrel coordinate sum: {game.barrel_gps_coordinates()}')


def input_to_direction(input_char: str) -> (int, int):
    if input_char == '<':
        return 0, -1
    if input_char == '>':
        return 0, 1
    if input_char == '^':
        return -1, 0
    if input_char == 'v':
        return 1, 0
    print(f'Invalid character "{input_char}"')
    return None


if __name__ == '__main__':
    main()
