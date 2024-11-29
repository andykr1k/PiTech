from Backend.Classes.Slot import Slot
from Backend.Classes.Container import Container


class Movement:
    def __init__(self, from_slot, to_slot, crane_position):

        self.from_slot = from_slot 
        self.to_slot = to_slot
        self.crane_position = crane_position # ending position after the move
        self.cost = 0

    def get_cost(self):
        return self.cost
    
    def heuristic_cost(self):
        pass

    def __repr__(self):
        return f"Move container from position ({self.from_slot}) to position {(self.to_slot)}, cost: {self.cost} minutes"
    
    def get_from_slot(self):
        return self.from_slot
    
    def get_to_slot(self):
        return self.to_slot
    
    def __lt__(self, other):
       return self.cost < other.cost

    