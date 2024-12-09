from Backend.Classes.Container import Container

import uuid

class Crane:
    def __init__(self, current_slot: Slot):
        
        self.position = position
        self.x = self.position[0]
        self.y = self.position[1]
        #self.grid_id = grid_id

    def __repr__(self):
        return f"crane grid, position: {self.grid_id}, {self.position}"
    

    def get_position(self):
        return self.position
    
    def set_position(self, position) -> None:
        self.position = position

    
