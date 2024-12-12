
class Container:
    # represent each container, include weight, name
    def __init__(self, name: str, weight: int, row: int, col: int):
        self.name = name
        self.weight = weight
        self.row = row
        self.col = col
        


    def __repr__(self):
        return f"{self.name}, {self.weight}, row: {self.row}, col: {self.col}"

    def get_weight(self):
        return self.weight
    
    def set_weight(self, weight):
        self.weight = weight
    
    def get_name(self):
        return self.name     

    def set_name(self, name):
        self.name = name
        return
    
    def set_position(self, row, col):
        self.row = row
        self.col = col
        return
    
    def get_position(self):
        return self.row, self.col
    
    def __eq__(self, other):
        if isinstance(other, Container):
            return (self.weight, self.name, self.row, self.col) == (other.weight, other.name, other.row, other.col)
        return False

    def __hash__(self):
         return hash((self.weight, self.name, self.row, self.col))
    
    def __lt__(self, other):
        if self.weight == other.weight:
            return self.name > other.name #this is reversed so this function can be used in SIFT. if two containers have same weights we place the higher ASCII on top
        return self.weight <other.weight