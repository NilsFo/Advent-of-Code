import numpy as np
import pandas as pd
import scipy
from numpy.ma.core import indices
from scipy.ndimage import label


class Arrangement:

    def __init__(self, plant_type, arrangement_map):
        super().__init__()
        self.plant_type = plant_type
        self.arrangement_map = arrangement_map

    def where(self):
        return np.where(self.arrangement_map == 1)

    def area(self) -> int:
        return len(self.where()[0])

    def perimeter(self) -> int:
        if self.area() == 1:
            return 4

        where = self.where()
        edges = []
        for i in range(len(where[0])):
            current_position = (where[0][i], where[1][i])

            local_edges = [
                is_arrangement_edge(self.arrangement_map, current_position, offset_x=1, offset_y=0),
                is_arrangement_edge(self.arrangement_map, current_position, offset_x=0, offset_y=1),
                is_arrangement_edge(self.arrangement_map, current_position, offset_x=-1, offset_y=0),
                is_arrangement_edge(self.arrangement_map, current_position, offset_x=0, offset_y=-1)
            ]

            # adding new edges to list, if they are not duplicates and only if they actually exist
            #edges.extend(e for e in local_edges if e is not None and e not in edges)
            edges.extend(e for e in local_edges if e is not None)

        return len(edges)


def is_arrangement_edge(arrangement_map: np.ndarray, current_position, offset_x, offset_y) -> (int, int):
    new_position = (
        current_position[0] + offset_x,
        current_position[1] + offset_y
    )

    rows, cols = arrangement_map.shape
    x, y = new_position

    if 0 <= x < rows and 0 <= y < cols:
        # check if out of bounds. if so, it's an edge
        if arrangement_map[new_position] == 0:
            return new_position
        else:
            return None

    # out of bounds, so a fence can be built
    return new_position


def main():
    f = open('input.txt')
    input = f.readlines()
    f.close()

    #####################
    # EXTRACTING PLANTS
    #####################

    # fining different types of plants
    plant_types: [str] = []
    garden_map = []
    for i, line in enumerate(input):
        line = line.strip()
        row = []

        for j, char in enumerate(line):
            if char not in plant_types:
                plant_types.append(char)
            row.append(char_to_number(char))

        garden_map.append(row)

    plant_types.sort()
    print(f'Number of plants: {len(plant_types)}. All plants: {plant_types}')

    #####################
    # EXTRACTING FIELDS
    #####################
    garden_map = np.array(garden_map, dtype=np.uint8)
    arrangements: [Arrangement] = []

    for i, plant_type in enumerate(plant_types):
        print(f'Finding masks for plant #{i + 1}: {plant_type}')
        type_id = char_to_number(plant_type)

        plant_mask = np.zeros(garden_map.shape, dtype=np.uint8)
        plant_mask[np.where(garden_map == type_id)] = 1

        # running connected component analysis
        #structure = np.ones((3, 3), dtype=int)
        structure = np.array([[0,1,0],[1,1,1],[0,1,0]],dtype=int)
        connected_components, component_indices = label(plant_mask, structure=structure)

        for j in range(1, component_indices + 1):
            arrangement_mask = np.zeros(garden_map.shape, dtype=np.uint8)
            arrangement_mask[np.where(connected_components == j)] = 1

            arrangements.append(Arrangement(plant_type, arrangement_mask))

    #####################
    # ANALYSING FIELDS
    #####################
    total_price = 0
    print(f'Number of arrangements: {len(arrangements)}')
    for arrangement in arrangements:
        area = arrangement.area()
        perimeter = arrangement.perimeter()
        print(f'Arrangement "{arrangement.plant_type}" price: {area}x{perimeter}={area * perimeter}')
        total_price += area * perimeter

    print(f'Total price: {total_price}')


def char_to_number(char):
    return ord(char.upper()) - ord('A')


if __name__ == '__main__':
    # too high 1471238
    main()
