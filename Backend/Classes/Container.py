
class Container:
    # represent each container, include weight, name
    def __init__(self, name: str, weight: int):
        self.name = name
        self.weight = weight

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
    
    def __eq__(self, other):
        if isinstance(other, Container):
            return self.weight == other.weight and self.name == other.name
        return False

    def __hash__(self):
        return hash((self.weight, self.name))