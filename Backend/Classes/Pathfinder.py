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
        self.valid_combinations = []
        pass    
    
    def balance(self):
        if(self.can_balance(self.start_state)):
            heapq.heappush(self.open_set, (0, 0, self.path, self.start_state))
            return self.balanceHelper()
        return self.sift()

    def balanceHelper(self):

        while self.open_set:
            f_cost, g_cost, path, state = heapq.heappop(self.open_set)
     
            if state.isBalanced():
                print('Balanced path found')
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
        #left_w, right_w, total_w = state.get_weights()
        #return abs(left_w - right_w)
        """
        Method 1 Misplaced contianers distance
        1. Find all the containers one the left side, for example, we have (100, 300) on the left side
        2. In the combinations right side we need (200,100,70)
        3. Calculate the cost needed to move container with weight (100) to the nearest available right side
        4. Same with the right side
        5. Sum up the distances cost
        If we have multiple goal combinations, we repeat step 1 to 5 and pick the one with minimum distance costs
        Method 2 Misplaced contianers 
        
        """
        best_heuristic_value = float('inf')
        for goal_combination in self.valid_combinations:
            heuristic_value = self.calculate_misplaced_heuristic(state, goal_combination)
            best_heuristic_value = min(best_heuristic_value, heuristic_value)
        
        return best_heuristic_value
        
    def calculate_misplaced_heuristic(self, state, goal_combination):
        
        side_a_weights, side_b_weights = set(goal_combination[0]), set(goal_combination[1])
        
        misplaced_1 = 0 
        misplaced_2 = 0
        for container in state.left_containers:
            weight = container.weight
            if weight not in side_a_weights:
                misplaced_1 += 1
            if weight not in side_b_weights:
                misplaced_2 += 1
                
        for container in state.right_containers:
            weight = container.weight
            if weight not in side_b_weights:
                misplaced_1 += 1
            if weight not in side_a_weights:
                misplaced_2 += 1


        return min(misplaced_1, misplaced_2)
    
    def can_balance(self, state):
        
        total_weight = state.total_weight
        weights = state.get_weightlist()
        lower_bound = round(total_weight / 2.1)
        upper_bound = round((1.1 / 2.1) * total_weight)
        can_balance = 0
        achievable = 1 
        sum_combinations = {0: []} 
        unique_combinations = set() 
        
        for weight in weights:
           
            new_combinations = {}
            for curr_sum in sum_combinations:
                new_sum = curr_sum + weight
                if new_sum not in sum_combinations:
                    new_combinations[new_sum] = sum_combinations[curr_sum] + [weight]
            for new_sum, combination in new_combinations.items():
                sum_combinations[new_sum] = combination

            achievable |= achievable << weight

        for target in range(lower_bound, upper_bound + 1):
            if (achievable >> target) & 1:
                side_a = sum_combinations[target]
                sorted_side_a = tuple(sorted(side_a))
                unique_combinations.add(sorted_side_a)
                can_balance = 1

        if can_balance:
            self.valid_combinations = []
            used_combinations = set()

            for combination in unique_combinations:
                remaining_weights = weights.copy()
                for weight in combination:
                    remaining_weights.remove(weight)

                side_b = tuple(sorted(remaining_weights))
                pair = tuple(sorted([combination, side_b]))

                if pair not in used_combinations:
                    self.valid_combinations.append((list(combination), list(side_b)))
                    used_combinations.add(pair)
            print(f"Balanceable! Combinations: {self.valid_combinations}")
            return can_balance
        
        else:
            print("Not balanceable.")
            return False
    
    def load():
        pass

    def unload():
        pass
    
    def sift(self):
        print("Sifting...")
        return []
        