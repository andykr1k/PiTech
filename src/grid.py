from cell import Cell
from container import Container
from movement import Movement

class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.columns = columns
        self.grid = [[None for _ in range(columns)] for _ in range(rows)]

    def setupGrid(self, manifest: str):
        
        #TODO: Implement manifest parsing logic and initialize grid using manifest values

        return

    def getCell(self, row: int, col: int) --> Cell:
        return self.grid[row][col]

    def setCell(self, row: int, col: int):
        self.grid[row][col] = Cell()

        return
    
    def getContainers(self) --> list[Container]:
        pass


    def display(self):
        pass

    def balance(self) --> list[Movement]:
        pass

    def load(self, container: Container, target: Cell) --> list[Movement]:
        pass

    def unload(self, container: Container)
        pass



    
 
