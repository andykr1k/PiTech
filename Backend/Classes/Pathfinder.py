from Backend.Classes.Slot import Slot
from Backend.Classes.Container import Container
from Backend.Classes.Grid import Grid
from Backend.Classes.Movement import Movement
import copy
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
                        new_f_cost = f_cost
                        if(move.from_slot==(6,4)and  move.to_slot==(1,6)):
                            crane_to_start_cost = state.calulate_path_cost(state.crane_position, move.from_slot)
                            move_cost = state.calulate_path_cost(move.from_slot, move.to_slot)
                        else:
                            crane_to_start_cost = state.calulate_path_cost(state.crane_position, move.from_slot)
                            move_cost = state.calulate_path_cost(move.from_slot, move.to_slot)
                        new_g_cost = g_cost + crane_to_start_cost + move_cost
                        #new_g_cost = g_cost + move.get_cost(child_state)
                        
                        h_cost = self.balance_heuristic(child_state)
                        new_f_cost += new_g_cost + h_cost
                        move.cost = crane_to_start_cost + move_cost
                        new_path = path + [move]

                        heapq.heappush(self.open_set, (new_f_cost, new_g_cost, new_path, child_state))
                        
        print("No balanced path found")
        return None
 
    def balance_heuristic(self, state):
        #left_w, right_w, total_w = state.get_weights()
        #return abs(left_w - right_w)

        best_heuristic_value = float('inf')
        for goal_combination in self.valid_combinations:
            heuristic_value = self.calculate_distance_heuristic(state, goal_combination)
            best_heuristic_value = min(best_heuristic_value, heuristic_value)
        
        return best_heuristic_value
    
    def calculate_distance_heuristic(self, state, goal_combination):
       
        side_a_weights, side_b_weights = set(goal_combination[0]), set(goal_combination[1])

        distance_1 = 0   
        distance_2 = 0
        
        for container in state.left_containers:
            if container.weight not in side_a_weights:
                row, col = container.get_position()
                target_position, min_distance = state.get_nearest_slot_on_other_side(row, col , 'right')
                if target_position:
                    distance_1 += min_distance
        for container in state.right_containers:
            if container.weight not in side_b_weights:
                row, col = container.get_position()
                target_position, min_distance = state.get_nearest_slot_on_other_side(row, col , 'left')
                if target_position:
                    distance_1 += min_distance
        
        for container in state.left_containers:
            if container.weight not in side_b_weights:
                row, col = container.get_position()
                target_position, min_distance = state.get_nearest_slot_on_other_side(row, col , 'right')
                if target_position:
                    distance_2 += min_distance
        for container in state.right_containers:
            if container.weight not in side_a_weights:
                row, col = container.get_position()
                target_position, min_distance = state.get_nearest_slot_on_other_side(row, col , 'left')
                if target_position:
                    distance_2 += min_distance
           

        return min(distance_1, distance_2)
     
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
            #print(f"Balanceable! Combinations: {self.valid_combinations}")
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

    def transfer(self):
        start_state_grid = self.start_state  # Initial state with crane at (8, 0)
        truck_start_state = copy.deepcopy(self.start_state) # Deep copy of the initial state
        truck_start_state.crane_position = (-1,-1)  # Set crane position to "truck"
        heapq.heappush(self.open_set, (0, 0, self.path, id(start_state_grid),start_state_grid))
        heapq.heappush(self.open_set, (0, 0, self.path, id(truck_start_state),truck_start_state))
        return self.transfer_helper()
    
    def transfer_helper(self):
        
        while self.open_set:
            f_cost, g_cost, path,_, state = heapq.heappop(self.open_set)
     
            if not state.unload_list and not state.load_list:
                print('Transfer path found')
                return path
            
            if state not in self.closed_set:
                self.closed_set.add(state)

                for child_state, move in state.get_possible_transfer_states_moves():
                    if child_state not in self.closed_set:
                        new_f_cost = f_cost
                        crane_to_start_cost = state.calulate_transfer_path_cost(state.crane_position, move.from_slot)
                        move_cost = state.calulate_transfer_path_cost(move.from_slot, move.to_slot)
                        new_g_cost = g_cost + crane_to_start_cost + move_cost
                        
                        h_cost = self.transfer_heuristic(child_state)
                        new_f_cost += new_g_cost + h_cost
                        move.cost = crane_to_start_cost + move_cost
                        new_path = path + [move]

                        heapq.heappush(self.open_set, (new_f_cost, new_g_cost, new_path, id(child_state),child_state))
                        
        print("No balanced path found")
        return None
    
    def transfer_heuristic(self, state):
        return 0
        