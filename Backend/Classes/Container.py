class Container:
    # represent each container, include weight, position, name
    def __init__(self, position, weight, name):
        self.position = position
        self.weight = weight
        self.name = name

    def __repr__(self):
        return f"{self.name}, {self.weight}"

    def update_position(self, new_position):
        self.position = new_position

    def get_weight(self):
        return self.weight
