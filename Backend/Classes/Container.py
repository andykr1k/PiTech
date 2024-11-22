
class Container:
    # represent each container, include weight, name
    def __init__(self, weight: int, name: str):
        self.weight = weight
        self.name = name

    def __repr__(self):
        return f"{self.name}, {self.weight}"

    def get_weight(self):
        return self.weight
    
    def get_name(self):
        return self.name
