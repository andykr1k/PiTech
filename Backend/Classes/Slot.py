from Backend.Classes.Container import Container
import uuid

class Slot:
    def __init__(self, grid_id: uuid.UUID, state=0, container: Container = None, position=(-1, -1)):
        # "NAN: 0", "UNUSED: 1", or "CONTAINER: 2"
        self.state = 0
        self.container = container
        self.position = position
        self.x = self.position[0]
        self.y = self.position[1]
        self.grid_id = grid_id

    def __repr__(self):
        return f"{self.position}, {self.state}, {self.container}\n-------------------------------\n"
    
    def get_container(self):
        return self.container
    
    def set_container(self, container: Container):
        self.container = container
        self.state = self.parseState()

    def remove_container(self):
        self.container = None
        self.state = 1

    def parseState(self):
        match self.container.get_name():
            case "NAN":
                return 0
            case "UNUSED":
                return 1
        return 2

    def __eq__(self, other):
        return self.grid_id == other.grid_id and self.position == other.position
    def __hash__(self):
        return hash((self.grid_id, self.position))