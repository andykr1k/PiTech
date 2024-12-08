
class Container:
    # represent each container, include weight, name
    def __init__(self, name: str, weight: int, row: int, col: int):
        self.name = name
        self.weight = weight
        self.row = row
        self.col = col

    def __repr__(self):
        return f"{self.name}, {self.weight}"

    def get_weight(self):
        return self.weight
    
    def set_weight(self, weight):
        self.weight = weight
    
    def get_name(self):
        return self.name     

    def set_name(self, name):
        self.name = name
        return   
    
    def get_position(self):
        return self.row, self.col
    
    def __eq__(self, other):
        if isinstance(other, Container):
            return (self.weight, self.name, self.row, self.col) == (other.weight, other.name, other.row, other.col)
        return False

    def __hash__(self):
         return hash((self.weight, self.name, self.row, self.col))