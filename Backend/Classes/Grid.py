
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
        self.right_weight = 0
        self.left_weight = 0
        self.total_weight = total_weight
        self.goal_weight = 0
        self.slot = [[Slot(grid_id=self.id, position=(i,j)) for j in range(columns)] for i in range(rows)]
        self.left_containers = set()
        self.right_containers = set()
        self.unload_list = [] # [Container]
        self.load_list = []   # [(name, weight)]
        self.crane_position = (8,0) # "truck" or (row,col)
        
    def get_slot(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            return self.slot[row][col]
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
                    row = int(manifestPosition[0]) -1
                    col = int(manifestPosition[1]) -1
                case 1:
                    containerWeight = int(manifestData[i][1:-1])
                case 2:
                    containerName = manifestData[i]
                    container = Container(containerName, containerWeight, row, col)
                    self.get_slot(row, col).set_container(container)
                    
                    if (self.slot[row][col].state==2):
                        if col < self.columns // 2:
                            self.left_containers.add(container)
                        else:
                            self.right_containers.add(container)
                    
        self.calculate_weights()
        return self.slot
    
    def get_grid(self):
        return self.slot
    
    def get_weights(self):
        return self.left_weight, self.right_weight, self.total_weight 
    
    def calculate_weights(self):
        # Note: hasn't considered empty container.
        self.left_weight = 0
        self.right_weight = 0
        for i in range(self.rows):
            for j in range(self.columns):
                slot = self.slot[i][j]
                if slot.state == 2:
                    if j < self.columns // 2:
                        self.left_weight += slot.container.get_weight()
                    else:
                        self.right_weight += slot.container.get_weight()
        self.total_weight = self.left_weight + self.right_weight
        return self.left_weight, self.right_weight, self.total_weight

    def isBalanced(self):
        lower_bound = round(self.total_weight / 2.1)
        upper_bound = round((1.1 / 2.1) * self.total_weight)
        # print(f"Balance range: {lower_bound} kg - {upper_bound} kg")
        self.goal_weight = (lower_bound, upper_bound)
        return lower_bound <= self.left_weight <= upper_bound

    def get_weightlist(self):
        weight = []
        for i in range(self.rows):
            for j in range(self.columns):
                slot = self.slot[i][j]
                if slot.state == 2:
                    weight.append(slot.container.get_weight())
        return weight
    
    def add_container(self, container, row, column):
        self.slot[row][column].container = container
        self.slot[row][column].state = 2  # Mark CONTAINER

    def remove_container(self, row, column):
        self.slot[row][column].container.set_name("UNUSED")
        self.slot[row][column].container.set_weight(0)
        self.slot[row][column].state = 1  # Mark UNUSED

    def move_container(self, pos1, pos2):
        # now only consider moving within the grid
        from_slot = self.get_slot(pos1[0], pos1[1])
        to_slot = self.get_slot(pos2[0], pos2[1])
        container = from_slot.get_container()
        name = container.get_name()
        weight = container.get_weight()
        self.update_container_lists(container, pos2)
        self.update_weight(pos1,add=False)
        from_slot.remove_container()
        to_slot.set_container(Container(name,weight,pos2[0],pos2[1]))
        self.update_weight(pos2,add=True)
        self.crane_position = pos2

    def get_movable_containers_position(self):
        # Returns the positions of all containers that can be moved (topmost in each column)
        movable_positions = []
        for j in range(self.columns):
            for i in range(self.rows - 1, -1, -1):
                slot = self.slot[i][j]
                if slot.state == 2:
                    movable_positions.append((i, j))
                    break
        return movable_positions 

    def get_valid_slots_position(self, pos1):
    # Returns a list of valid slot positions where a container can be moved
        valid_slot_position = []
        curr_col = pos1[1]
        for j in range(self.columns):  # Iterate over each column
            if j == curr_col:  # Skip the current column of the container
                continue
            for i in range(self.rows):  # Iterate from bottom (row 0) to top
                slot = self.slot[i][j]
                if slot.state == 1:  # If the slot is UNUSED
                    valid_slot_position.append((i, j))  # Add the first UNUSED slot
                    break 
    
        return valid_slot_position
    
    def get_nearest_slot_on_other_side(self, row, col, target_side):

        min_distance = float('inf')
        nearest_slot = None

        if target_side == 'left':
            target_columns = range(0, self.columns // 2) 
        elif target_side == 'right':
            target_columns = range(self.columns // 2, self.columns) 
        else:
            raise ValueError("target_side must be either 'left' or 'right'")

        for target_col in target_columns:
            for target_row in range(self.rows):  
                slot = self.slot[target_row][target_col]
                if slot.state == 1:  
                    distance = abs(row - target_row) + abs(col - target_col)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_slot = (target_row, target_col)
                    break

        return nearest_slot, min_distance
    
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
                
                move = Movement(from_slot = starting_position, to_slot = destination, crane_position = destination)
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
        for row in self.slot:
            for slot in row:
                container_name = slot.container.get_name() 
                container_weight = slot.container.get_weight()
                res += f"Position: {slot.position}, State: {slot.state}, Container Name: {container_name}, Container Weight: {container_weight}\n"
                res += '-'*40 + '\n'
        return res

    def get_slot(self, row, col):
        return self.slot[row][col]

    def update_weight(self, pos, add=True):
        """
        We can add a container from a car, remove a container from the ship,
        or move a container within the ship's bay. The weights will be updated accordingly.
        """
        # add: add or subtract the container's weight.
        slot = self.slot[pos[0]][pos[1]]
        if slot.state == 2 and slot.container is not None: 
            container_weight = slot.container.get_weight() 
            if pos[1] < self.columns//2:  
                if add:
                    self.left_weight += container_weight
                    self.total_weight += container_weight
                else:
                    self.left_weight -= container_weight
                    self.total_weight -= container_weight 
            else:  
                if add:
                    self.right_weight += container_weight
                    self.total_weight += container_weight
                else:
                    self.right_weight -= container_weight
                    self.total_weight -= container_weight 
    
    def update_container_lists(self, container, pos2):
        # Handle balance within the grid, no sifting or to buffer
        container_copy = copy.deepcopy(container)
        container_copy.row=pos2[0]
        container_copy.col=pos2[1]
        if container in self.left_containers:
            self.left_containers.remove(container)
        else:
            self.right_containers.remove(container)
        if pos2[1] < self.columns // 2:
            self.left_containers.add(container_copy)
        else:  
            self.right_containers.add(container_copy)

                        
    def __eq__(self, other):
        if isinstance(other, Grid):
            return (
                self.right_weight == other.right_weight and
                self.left_weight == other.left_weight and
                self.grid_as_tuple() == other.grid_as_tuple()
            )
        return False

    def __hash__(self):
        return hash((
            self.right_weight,
            self.left_weight,
            self.grid_as_tuple()
        ))
        
    def calulate_path_cost(self, pos1, pos2):
        
        # If pos1 is "truck", move from the truck to (8, 0)
        if pos1 == "truck":
            distance += 2  # Add 2 minutes to move from the truck to (8, 0)
            pos1 = (8, 0)  # Update pos1 to the crane's entry point on the grid

         # If pos2 is "truck", move from (8, 0) to the truck after reaching (8, 0)
        if pos2 == "truck":
            distance_to_truck = self.calculate_path_cost(pos1, (8, 0))
            return distance_to_truck + 2
        
        current_row = pos1[0]
        current_col = pos1[1]
        target_row = pos2[0]
        target_col = pos2[1]
        distance = 0
  
        # Special case: Starting from (8, 0)
        if current_row == 8:
            return distance + abs(current_col - target_col) + abs(current_row - target_row)

        # General: Move within the grid
        while current_col != target_col:
            next_col = current_col + (1 if target_col > current_col else -1)

            if next_col == target_col and current_row == target_row:
                distance += 1
                break
            
            # Check for obstacles in the next column
            while self.get_slot(current_row, next_col).state != 1:  # Obstacle
                if current_row < self.rows - 1:
                    current_row += 1
                    distance += 1
                else:
                    # Imaginary row, move across
                    distance += 1
                    break 

            current_col = next_col
            distance += 1

        while current_row < target_row:
            current_row += 1
            distance += 1
        while current_row > target_row:
            current_row -= 1
            distance += 1

        return distance

    def grid_as_tuple(self):
        return tuple(
            tuple(
                (slot.state, slot.container) for slot in row
            ) for row in self.slot
        )
        
    def setup_transferlist(self, tranfser_list):
        for command in tranfser_list:
            parts = command.strip().split(',')
            operation = parts[0]
            
            if operation == 'load':
                name = parts[1]
                weight = int(parts[2])
                self.load_list.append((name, weight))
            elif operation == 'unload':
                name = parts[1]
                container = self.find_container_by_name(name)
                self.unload_list.append(container)
    
    def find_container_by_name(self, name):
        for container in self.left_containers:
            if container.name == name:
                return container
        for container in self.right_containers:
            if container.name == name:
                return container
    def getPossibleTransferMoves(self):
        possible_moves = []
        # Handle load
        if self.load_list:  # Check if there are items to load
            name, weight = self.load_list[0]  # Pick the first item to load
            valid_slots = self.get_valid_slots_position(None)  # Find all valid slots
            for target_position in valid_slots:
                move = Movement(from_slot="truck", to_slot=self.get_slot(*target_position), crane_position=self.target_position)
                possible_moves.append(move)
                break
            
         # Handle unload 
        for container in self.unload_list:
            if self.can_unload(container):
                move = Movement(from_slot=self.get_slot(container.row, container.col), to_slot="truck", crane_position="truck")
                possible_moves.append(move)
            else:
                block_container = self.get_topmost_blocking_container(container)
                valid_slots = self.get_valid_slots_position((block_container.row, block_container.col))
                for destination in valid_slots:
                    # Generate a single move to remove the topmost blocker
                    move = Movement(
                        from_slot=self.get_slot(block_container.row, block_container.col),
                        to_slot=self.get_slot(*destination),
                        crane_position=self.destination
                    )
                    possible_moves.append(move)
                    break 
         
         

        return possible_moves
        
        pass
    def getPossibleTransferStatesMoves(self):
        
        neighbor_states_moves = []
        possible_moves = self.getPossibleTransferMoves()
        for move in possible_moves:
            new_grid = copy.deepcopy(self)
            new_grid.move_container(move.from_slot, move.to_slot)
            neighbor_states_moves.append((new_grid, move))
            
        return neighbor_states_moves
   
