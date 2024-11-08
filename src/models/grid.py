from .slot import Slot
from .container import Container

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