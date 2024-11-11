from cell import Cell

class Movement:
    def __init__(self, from: Cell, to: Cell, cost: int):
        self.from = from
        self.to = to
        self.cost = cost