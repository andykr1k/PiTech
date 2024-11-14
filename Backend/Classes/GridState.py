from Classes.Slot import Slot
from Classes.Container import Container
import copy

# Constants
EMPTY_CONTAINER_WEIGHT = 4200

class GridState:
    def __init__(self, total_weight=0, goal_weight=0, rows=8, columns=12):
        self.rows = rows
        self.columns = columns
        self.cost = 0  # each time we move_container, the cost will be calculated and updated
        self.right_weight = 0
        self.left_weight = 0
        self.total_weight = total_weight
        self.goal_weight = 0
        self.grid = [[Slot(position=(i, j))
                      for j in range(columns)] for i in range(rows)]

    def setup_grid(self, manifestData):
        count = 0
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                parsed = manifestData[count].split(", ")
                slot = Slot()
                if len(parsed) == 3:
                    slot.position = (i+1, j+1)
                    number = parsed[1][1:-1]
                    starting_index = 0

                    for k in range(len(number)):
                        if number[k] != '0':
                            break
                        starting_index += 1

                    number_cast = number[starting_index:]
                    if len(number_cast) == 0:
                        slot.weight = 0
                    else:
                        slot.weight = int(number_cast)
                    if parsed[2].strip() == "NAN":
                        slot.state = 0
                    elif parsed[2].strip() == "UNUSED":
                        slot.state = 1
                    else:
                        slot.state = 2
                        slot.container = Container(
                            slot.position, slot.weight, parsed[2])

                    count += 1
                    self.grid[i][j] = slot
        return self.grid

    def calculate_weights(self):
        # Note: hasn't considered empty container.
        self.left_weight = 0
        self.right_weight = 0
        for i in range(self.rows):
            for j in range(self.columns):
                slot = self.grid[i][j]
                if slot.state == 2:
                    if j < self.columns // 2:
                        self.left_weight += EMPTY_CONTAINER_WEIGHT + slot.container.get_weight()
                    else:
                        self.right_weight += EMPTY_CONTAINER_WEIGHT + slot.container.get_weight()
        self.total_weight = self.left_weight + self.right_weight
        return self.left_weight, self.right_weight, self.total_weight

    def isBalanced(self):
        lower_bound = round(self.total_weight / 2.1)
        upper_bound = round((1.1 / 2.1) * self.total_weight)
        print(f"Balance range: {lower_bound} kg - {upper_bound} kg")
        self.goal_weight = (lower_bound, upper_bound)
        return lower_bound <= self.left_weight <= upper_bound

    def add_container(self, container, row, column):
        self.grid[row][column].container = container
        self.grid[row][column].state = 2  # Mark CONTAINER

    def remove_container(self, row, column):
        self.grid[row][column].container = None
        self.grid[row][column].state = 1  # Mark UNUSED

    def move_container(self, pos1, pos2):
        container = self.grid[pos1[0]][pos1[1]].container
        self.remove_container(pos1[0], pos1[1])
        self.add_container(container, pos2[0], pos2[1])
        container.update_position(pos2)

    def calculate_cost(self, pos1, pos2):
        heuristic_cost = 0
        # Placeholder
        return heuristic_cost + self.manhattan_distance(pos1, pos2)

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def expand(self):
        # Return a list of children girds
        children = []
        # 1. Gets movable containers
        movable_containers_position = self.get_movable_containers_position()
        for pos1 in movable_containers_position:
            # 2. For each movable get valid slots to move to
            valid_slots = self.get_valid_slots_position(pos1)
            for pos2 in valid_slots:
                # 3. Generate such grid (move from pos1 to pos2) and update the cost
                # Note: Fix later for better efficiency.
                new_grid = copy.deepcopy(self)
                new_grid.move_container(pos1, pos2)
                move_cost = self.calculate_cost(pos1, pos2)
                new_grid.cost = self.cost + move_cost
                # 4. Apped the grid to the children list
                children.append(new_grid)

        return children

    def get_movable_containers_position(self):
        # Returns the positions of all containers that can be moved (topmost in each column)
        movable_positions = []
        for j in range(self.columns):
            for i in range(self.rows - 1, -1, -1):
                slot = self.grid[i][j]
                if slot.state == 2:
                    movable_positions.append((i, j))
                    break
        return movable_positions

    def get_valid_slots_position(self, pos1):
        # Returns a list of valid slot position where a container can be moved
        valid_slot_position = []
        curr_col = pos1[1]-1
        for i in range(self.rows):
            for j in range(self.columns):
                if j == curr_col:  # Skip the column of the container's current position
                    continue
                slot = self.grid[i][j]
                if slot.state != 1:  # Check if the slot is UNUSED
                    continue
                if i == 0:  # Valid if it's in the first row
                    valid_slot_position.append((i, j))
                    continue
                if i > 0 and self.grid[i - 1][j].state != 1:  # Valid if it's not directly above an UNUSED slot
                    valid_slot_position.append((i, j))
                    continue
        return valid_slot_position

    def print_path(self, goal_state):
        # Placeholder"
        return 0

    def __repr__(self):
        result = ""
        for row in self.grid:
            for slot in row:
                result += str(slot)
        return result

    def __lt__(self, other):
        # This allows GridState to be sotred in heapq according to the cost
        return self.cost < other.cost
