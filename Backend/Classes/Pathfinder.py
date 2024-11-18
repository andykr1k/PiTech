from Backend.Classes.Slot import Slot
from Backend.Classes.Container import Container
from Backend.Classes.Grid import Grid
from Backend.Classes.Movement import Movement
import heapq

class Pathfinder():
    def __init__(self, current_grid):
        self.open_set = []
        self.closed_set = set()
        self.start_state = current_grid
        self.path = []
        pass    

    def balance(self):
        heapq.heappush(self.open_set, (0, 0, self.path, self.start_state))
        return self.balanceHelper()

    def balanceHelper(self):
        while self.open_set:
            f_cost, g_cost, path, state = heapq.heappop(self.open_set)

            if state.isBalanced():
                print('Balanced path found: ', path)
                return path

            if state not in self.closed_set:
                self.closed_set.add(state)

                for child_state, move in state.getPossibleStatesMoves():
                    if child_state not in self.closed_set:
                        new_g_cost = g_cost + move.get_cost()
                        h_cost = self.balance_heuristic(child_state)
                        new_f_cost = new_g_cost + h_cost
                        new_path = path + [move]

                        heapq.heappush(self.open_set, (new_f_cost, new_g_cost, new_path, child_state))

        print("No balanced path found")
        return None


    def balance_heuristic(self, state):
        left_w, right_w, total_w = state.calculate_weights()
        return abs(left_w - right_w)

    def load():
        pass

    def unload():
        pass