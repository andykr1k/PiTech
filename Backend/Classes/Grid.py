
from Backend.Classes.Slot import Slot
from Backend.Classes.Container import Container
from Backend.Classes.Movement import Movement
import copy
import uuid

class Grid:
    def __init__(self, total_weight=0, goal_weight=0, rows=8, columns=12, id=uuid.uuid4()):
        self.rows = rows
        self.columns = columns
        self.id = id
        # self.cost = 0  # each time we move_container, the cost will be calculated and updated
        self.right_weight = 0
        self.left_weight = 0
        self.total_weight = total_weight
        self.goal_weight = 0
        self.grid = [[Slot(grid_id=self.id, position=(i,j)) for j in range(columns)] for i in range(rows)]

    def get_slot(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            return self.grid[row][col]
        else:
            raise IndexError("Slot position out of grid bounds")

    def setup_grid(self, manifestData):
        row = 0
        col = 0
        containerName = ""
        containerWeight = 0
        for i in range(len(manifestData)):
            condition = i % 3
            match condition:
                case 0:
                    manifestPosition = str(manifestData[i])[1:-1].strip().split(",")
                    row = int(manifestPosition[0]) - 1
                    col = int(manifestPosition[1]) - 1
                case 1:
                    containerWeight = int(manifestData[i][1:-1])
                case 2:
                    containerName = manifestData[i]
                    self.get_slot(row, col).set_container(Container(containerWeight, containerName))
        self.calculate_weights()
        return self.grid
    
    def get_grid(self):
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
                        self.left_weight += slot.container.get_weight()
                    else:
                        self.right_weight += slot.container.get_weight()
        self.total_weight = self.left_weight + self.right_weight
        return self.left_weight, self.right_weight, self.total_weight

    def isBalanced(self):

        #self.left_weight, self.right_weight, self.total_weight = self.calculate_weights()
        lower_bound = round(self.total_weight / 2.1)
        upper_bound = round((1.1 / 2.1) * self.total_weight)
        # print(f"Balance range: {lower_bound} kg - {upper_bound} kg")
        self.goal_weight = (lower_bound, upper_bound)
        return lower_bound <= self.left_weight <= upper_bound

    def add_container(self, container, row, column):
        self.grid[row][column].container = container
        self.grid[row][column].state = 2  # Mark CONTAINER

    def remove_container(self, row, column):
        self.grid[row][column].container = None
        self.grid[row][column].state = 1  # Mark UNUSED

    def move_container(self, pos1, pos2):
        from_slot = self.get_slot(pos1[0], pos1[1])
        to_slot = self.get_slot(pos2[0], pos2[1])
        container = from_slot.get_container()
        from_slot.remove_container()
        to_slot.set_container(container)
        print(f'Container: {container} moved from {from_slot} to {to_slot}')

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
    # Returns a list of valid slot positions where a container can be moved
        valid_slot_position = []
        curr_col = pos1[1]
        for j in range(self.columns):
            if j == curr_col:  # Skip the column of the container's current position
                continue
            for i in range(self.rows - 1, -1, -1):
                slot = self.grid[i][j]
                if slot.state == 1:  # Check if the slot is UNUSED
                    if i == self.rows - 1 or self.grid[i + 1][j].state != 1:  # Valid if it's the bottom slot or the slot below is not UNUSED
                        valid_slot_position.append((i, j))
                        break
        return valid_slot_position
    
    
    def getPossibleMoves(self):
        """
        Generate a list of all possible moves for movable containers.
        This method identifies all movable containers and their valid destination slots,
        then creates a list of Movement objects representing each possible move.
        Returns:
            List[Movement]: A list of possible moves, where each move is represented
            by a Movement object with 'from_slot' as the starting position and 'to_slot'
            as the destination position.
        """
        possible_moves = []
        movable_containers_position = self.get_movable_containers_position()
        for starting_position in movable_containers_position:
            valid_slots = self.get_valid_slots_position(starting_position)
            for destination in valid_slots:
                
                move = Movement(from_slot = starting_position, to_slot = destination)
                possible_moves.append(move)
        return possible_moves

    def getPossibleStatesMoves(self): 
        """
        Generates all possible states and their corresponding moves from the current grid state.

        This method first retrieves all possible moves from the current grid state. For each possible move,
        it creates a deep copy of the current grid, applies the move to the copied grid, and then appends
        the new grid state along with the move to a list. The list of all possible new grid states and their
        corresponding moves is then returned.

        Returns:
            list of tuple: A list where each element is a tuple containing a new grid state (after a move)
                           and the move that was applied to reach that state.
        """
        neighbor_states_moves = []
        possible_moves = self.getPossibleMoves()
        for move in possible_moves:
            new_grid = copy.deepcopy(self)
            new_grid.move_container(move.from_slot, move.to_slot)
            neighbor_states_moves.append((new_grid, move))
        return neighbor_states_moves
   
    def print_path(self, goal_state):
        # Placeholder"
        return 0

    def __repr__(self):
        res = ""
        for row in self.grid:
            for slot in row:
                res += str(slot)
        return res

    def get_slot(self, row, col):
        return self.grid[row][col]


