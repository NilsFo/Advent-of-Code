class Station:

    def __init__(self, position: (int, int), signal: str):
        super().__init__()
        self.position = position
        self.signal = signal

    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]


class AntiStation:

    def __init__(self, position: (int, int)):
        super().__init__()
        self.position = position

    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

    def inside_board(self, board_width, board_height):
        return 0 <= self.x() < board_width and 0 <= self.y() < board_height


def main():
    f = open('input.txt', 'r')
    input = f.readlines()
    f.close()

    signals: list[str] = []
    station_dict: dict[list[Station]] = {}
    all_stations: list[Station] = []
    anti_stations: list[AntiStation] = []

    board_width = 0
    board_height = 0
    remove_duplicates = True

    for i, line in enumerate(input):
        line = line.strip()
        for j, character in enumerate(line):
            board_width = i + 1
            board_height = j + 1

            if character != '.':

                if character not in signals:
                    station_dict[character] = []
                    signals.append(character)

                s = Station((i, j), character)
                all_stations.append(s)
                station_dict[character].append(s)

    del input, i, j, character
    print(f'Board size: {board_width}x{board_height}')

    signals.sort()
    print(f'List of signals: {signals}')
    print('')
    print_board(
        board_width=board_width,
        board_height=board_height,
        stations=all_stations,
        anti_stations=[]
    )

    #######################################################################

    for signal in signals:
        current_stations: [Station] = station_dict[signal]
        anti_stations.extend(calculate_anti_stations(current_stations))

    for i in reversed(range(len(anti_stations))):
        anit_station: AntiStation = anti_stations[i]
        if not anit_station.inside_board(board_width, board_height):
            del anti_stations[i]
            continue

        if remove_duplicates:
            duplicate = False
            for j in reversed(range(len(anti_stations))):
                other_station = anti_stations[j]
                if i != j:
                    if anit_station.x() == other_station.x() and anit_station.y() == other_station.y():
                        print(f'Removing duplicate station at {anit_station.position}')
                        duplicate = True
            if duplicate:
                del anti_stations[i]
                continue

    #######################################################################

    print_board(
        board_width=board_width,
        board_height=board_height,
        stations=all_stations,
        anti_stations=anti_stations
    )

    print('')
    print(f'Number of stations: {len(anti_stations)}')


def print_board(board_width: int, board_height: int, stations: list[Station], anti_stations: [AntiStation]):
    for i in range(board_width):
        for j in range(board_height):
            character = '.'

            for station in anti_stations:
                if station.x() == i and station.y() == j:
                    character = '#'

            for station in stations:
                if station.x() == i and station.y() == j:
                    character = station.signal

            print(character, end='')

        print('\n', end='')

    print('')


def calculate_anti_stations(stations: [Station]):
    anti_stations: list[AntiStation] = []

    for i, current_station in enumerate(stations):
        for j, other_station in enumerate(stations):
            if i != j:
                if current_station.x() < other_station.x():
                    continue

                dx = other_station.x() - current_station.x()
                dy = other_station.y() - current_station.y()

                for r in range(50):
                    r += 0
                    anti_stations.append(AntiStation(
                        (
                            current_station.x() - dx * r,
                            current_station.y() - dy * r
                        )
                    ))
                    anti_stations.append(AntiStation(
                        (
                            other_station.x() + dx * r,
                            other_station.y() + dy * r
                        )
                    ))

    return anti_stations


if __name__ == '__main__':
    main()
