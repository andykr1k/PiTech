from Backend.Classes.Slot import Slot

class Movement:
    def __init__(self, from_slot: Slot, to_slot: Slot):

        self.from_slot = from_slot 
        self.to_slot = to_slot
        self.cost = 0
    
    def get_from_slot(self):
        return self.from_slot
    
    def get_to_slot(self):
        return self.to_slot
    
    def get_cost(self):
        return self.cost
    
    def heuristic_cost(self):
        pass

    def __repr__(self):
        from_slot = "truck" if self.from_slot.position == (-1, -1) else self.from_slot.position
        to_slot = "truck" if self.to_slot.position == (-1, -1) else self.to_slot.position
        return f"Move container from position {from_slot}, grid: {self.from_slot.get_grid_id()} to position {to_slot}, grid: {self.from_slot.get_grid_id()}, Time estimation: {self.cost} minutes"
    
    
    def __lt__(self, other):
       return self.cost < other.cost

    