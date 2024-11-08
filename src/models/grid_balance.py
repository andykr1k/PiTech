
class Container:
    # represent each container, include weight, position, name
    def __init__(self, position, weight, name):
        self. position = position
        self.weight = weight
        self.name = name
        
    def __repr__(self):
        return f"Container(name={self.name}, weight={self.weight}, position={self.position})"
    
    def update_position(self, new_position):
        self.position = new_position
        
    def get_weight(self):
        return self.weight
    
class Slot:
    def __init__(self, state="UNUSED", container=None, position=None):
        # "NAN", "UNUSED", or "CONTAINER"
        self.state = state 
        self.container = container
        self.position = position

    def __repr__(self):
        if self.container:
            return f"{self.container}"
        return self.state
    
class Grid:
    
    def __init__(self, rows=6, columns=6):
        self.rows = rows
        self.columns = columns
        self.grid = [[None for _ in range(columns)] for _ in range(rows)]
        
    def setup_grid(self, manifest):
        return 0
    
    def add_container(self, container, row, column):
        self.grid[row][column] = container
        
    def remove_container(self, row, column):
        self.grid[row][column] = None
        
    def isBalanced(self):
        return 0
    def get_weights():
        return 0
    
def manhattan_distance(self, pos1, pos2):
    return 0

def expand(self):
    return 0

def print_path(self, goal_state):
    return 0