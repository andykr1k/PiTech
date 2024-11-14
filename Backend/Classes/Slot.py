class Slot:
    def __init__(self, state=0, container=None, position=(-1, -1)):
        # "NAN: 0", "UNUSED: 1", or "CONTAINER: 2"
        self.state = state
        self.container = container
        self.position = position

    def __repr__(self):
        return f"{self.position}, {self.state}, {self.container}\n-------------------------------\n"
