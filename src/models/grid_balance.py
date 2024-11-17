import copy
EMPTY_CONTAINER_WEIGHT = 4200

class Container:
    # represent each container, include weight, position, name
    def __init__(self, position, weight, name):
        self.position = position
        self.weight = weight
        self.name = name
        
    def update_position(self, new_position):
        self.position = new_position
        
    def get_weight(self):
        return self.weight
    
    def __eq__(self, other):
        if isinstance(other, Container):
            return (self.position == other.position and 
                    self.weight == other.weight and 
                    self.name == other.name)
        return False
    
    def __hash__(self):
        return hash((self.position, self.weight, self.name))
    
    def __repr__(self):
        return f"{self.name}, {self.weight}"
    
        
class Slot:
    def __init__(self, state= 0, container=None, position=(-1,-1)):
        # "NAN: 0", "UNUSED: 1", or "CONTAINER: 2"
        self.state = state 
        self.container = container
        self.position = position
        
    def __repr__(self):
        if self.state == 0:
            state_str = "NAN"
        elif self.state == 1:
            state_str = "UNUSED"
        elif self.state == 2 and self.container is not None:
            state_str = "CONTAINER"
            
        return f"{self.position}, {state_str}, Container: {self.container}\n-------------------------------\n"

    def __eq__(self, other):
        if isinstance(other, Slot):
            return (self.state == other.state and
                    self.position == other.position and
                    self.container == other.container)
        return False

    def __hash__(self):
        return hash((self.state, self.position, self.container))   

class GridState:
    
    def __init__(self,total_weight=0, goal_weight=0, rows=8, columns=12 ):
        self.rows = rows
        self.columns = columns
        self.cost = 0 # each time we move_container, the cost will be calculated and updated
        self.right_weight = 0
        self.left_weight = 0
        self.total_weight = total_weight
        self.goal_weight = 0
        self.grid = [[Slot(position=(i, j)) for j in range(columns)] for i in range(rows)]
           
    def setup_grid(self, manifest):
        with open(manifest) as f:
            data = f.readlines()

        count = 0
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                    parsed = data[count].split(", ")
                    slot = Slot()
                    if len(parsed) == 3:
                        slot.position = (i+1,j+1)
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
                            slot.container = Container(slot.position, slot.weight, parsed[2])                   
                    
                    count += 1
                    self.grid[i][j] = slot
                    
        self.calculate_weights()
    
    def calculate_weights(self):
        # Note: hasn't considered empty container.
        # When setting up a grid with manifess, calculate left, right, total and goal weight range.
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
        lower_bound = round(self.total_weight / 2.1)
        upper_bound = round((1.1 / 2.1) * self.total_weight)
        print(f"Balance range: {lower_bound} kg - {upper_bound} kg")
        self.goal_weight = (lower_bound, upper_bound)
        return self.left_weight, self.right_weight, self.total_weight, self.goal_weight
    
    def isBalanced(self):
        return self.goal_weight[0] <= self.left_weight <= self.goal_weight[1] 
         
    """
    We can add a container from a car, remove a container from the ship,
    or move a container within the ship's bay. The weights will be updated accordingly.
    """
    def update_weight(self, pos, add=True):
        # add: add or subtract the container's weight.
        slot = self.grid[pos[0]][pos[1]]
        if slot.state == 2 and slot.container is not None: 
            container_weight = slot.container.get_weight() + EMPTY_CONTAINER_WEIGHT
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
           
    def add_container(self, container, pos):
        slot = self.grid[pos[0]][pos[1]]
        container.update_position(pos)
        slot.container= container
        slot.state= 2 # Mark CONTAINER
        self.update_weight(pos, add=True)
        
    def remove_container(self, pos):
        self.update_weight(pos, add=False)
        slot = self.grid[pos[0]][pos[1]]
        slot.container = None
        slot.state = 1 # Mark UNUSED
        
    def move_container(self, pos1, pos2):
        container = self.grid[pos1[0]][pos1[1]].container
        self.remove_container(pos1)
        self.add_container(container, pos2)
        
    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])  
      
    def calculate_cost(self, pos1, pos2):
        heuristic_cost = 0
        # Placeholder
        return heuristic_cost + self.manhattan_distance(pos1, pos2)
    
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
                if slot.state != 1: # Check if the slot is UNUSED
                    continue
                if i == 0: # Valid if it's in the first row
                    valid_slot_position.append((i, j))
                    continue
                if i>0 and self.grid[i - 1][j].state != 1: # Valid if it's not directly above an UNUSED slot
                    valid_slot_position.append((i, j))
                    continue  
                               
        return valid_slot_position
    
    def expand(self): 
        # Note: the buffer area is not considered yet
        # Return a list of children girds generated by moving containers
        children = []
        # 1. Gets movable containers
        movable_containers_position = self.get_movable_containers_position()
        for pos1 in movable_containers_position:
            # 2. For each movable get valid slots to move to
            valid_slots = self.get_valid_slots_position(pos1)
            for pos2 in valid_slots:

                # 3. Generate such grid (move from pos1 to pos2) and update the cost
                new_grid = copy.deepcopy(self) # Note: Fix later for better efficiency. 
                new_grid.move_container(pos1, pos2)
                
                move_cost = self.calculate_cost(pos1, pos2)
                new_grid.cost = self.cost + move_cost
                # 4. Apped the grid to the children list
                children.append(new_grid)
             
        return children

    def print_path(self, goal_state):
        # Placeholder"
        return 0
    
    def get_weight(self):
        return self.left_weight, self.right_weight, self.total_weight, self.goal_weight
    
    def __repr__(self):
        result = ""
        for row in self.grid:
            for slot in row:
                result += str(slot)
        return result
    
    def __lt__(self, other):
        return self.cost < other.cost # This allows GridState to be sotred in heapq according to the cost
    
    def __eq__(self, other):
        if isinstance(other, GridState):
            # Two GridState objects are equal if their grid, cost, and weights are the same
            return (self.cost == other.cost and
                    self.grid == other.grid and
                    self.left_weight == other.left_weight and
                    self.right_weight == other.right_weight and
                    self.total_weight == other.total_weight and
                    self.goal_weight == other.goal_weight)
        return False
    
    def __hash__(self):
        # Hashing grid, slots and containers, 3 of them together is a hash key.
        # This enables O(1) checks to determine if a grid configuration already existed
        grid_hash = hash(tuple(hash(tuple(slot for slot in row)) for row in self.grid))
        return hash((self.cost, self.left_weight,
                     self.right_weight, self.total_weight, self.goal_weight, grid_hash))
"""       
#Testing 
grid = GridState(rows=4, columns=6)
#grid.setup_grid("../../manifests/sample_manifest_notbalanced.txt")
#grid.setup_grid("../../manifests/sample_manifest_balanced.txt")
grid.setup_grid("../../manifests/sample_manifest_children_test.txt")
print(grid)
x, y, z, w = grid.calculate_weights()
print(f"Weight: {x, y, z}, Goal weight: {w}")
print(f"Is_balanced: {grid.isBalanced()}")
#check get_movable_containers_position
position = grid.get_movable_containers_position()
position_display = [(i + 1, j + 1) for i, j in position]
print(f"Available container to move: {position_display}")

#check get_valid_slots_position
slots = grid.get_valid_slots_position((3,1))
slots_display = [(i + 1, j + 1) for i, j in slots]
print(f"Available slots to move container (3, 1): {slots_display}")

#check expanded states and weights
children = grid.expand()
print(f"Numbers of children: {len(children)}")
for i in range(3):
    grid = children[i]
    x, y, z, w = grid.calculate_weights()
    print(f"Weight: {x, y, z}, Goal weight: {w}")
    print(f"Is_balanced: {grid.isBalanced()}")
"""