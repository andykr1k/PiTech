from Backend.Classes.Slot import Slot
from Backend.Classes.Container import Container


class Movement:
    def __init__(self, from_slot: Slot, to_slot: Slot):

        self.from_slot = from_slot
        self.to_slot = to_slot
        self.manh_cost = self.manhattan_distance()

    def get_cost(self):
        self.manh_cost = self.manhattan_distance()
        return self.manh_cost
    
    def manhattan_distance(self):
        start_slot = self.get_from_slot()
        end_slot = self.get_to_slot()
        distance = abs(start_slot[0] - end_slot[0]) + abs(start_slot[1] - end_slot[1])
        return distance
    
    def heuristic_cost(self):
        pass

    def __repr__(self):
        return f"Move container from position ({self.from_slot[0] }, {self.from_slot[1] }) to position ({self.to_slot[0] }, {self.to_slot[1] })"
    
    def get_from_slot(self):
        return self.from_slot
    
    def get_to_slot(self):
        return self.to_slot
    
    def __lt__(self, other):
        return self.get_cost() < other.get_cost()

    