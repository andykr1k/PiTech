class Container:
    # represent each container, include weight, position, name
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def __repr__(self):
        return f"Container(name={self.name}, weight={self.weight})"