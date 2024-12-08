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
        
        else:
            print("Beginning SIFT Operation")
            return self.sift()

    def balanceHelper(self):

        while self.open_set:
            f_cost, g_cost, path, state = heapq.heappop(self.open_set)
     
            if state.isBalanced():

                current_grid = self.start_state
                path_with_intermediate_grids = self.reconstruct_grids_from_path(current_grid, path)

                return path_with_intermediate_grids

            if state not in self.closed_set:
                self.closed_set.add(state)

                for child_state, move in state.getPossibleStatesMoves():
                    if child_state not in self.closed_set:
                        new_f_cost = f_cost
                        crane_to_start_cost = state.calculate_path_cost(state.crane_position, move.from_slot)
                        move_cost = state.calculate_path_cost(move.from_slot, move.to_slot)
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
    
    def reconstruct_grids_from_path(self, current_grid, path):

        moves_intermediate_grids = []
        grid_copy = copy.deepcopy(current_grid)

        last_crane_pos = path[-1].to_slot
        default_crane_pos = (8,0)
        last_cost = abs(last_crane_pos[0] - default_crane_pos[0]) + abs(last_crane_pos[1] - default_crane_pos[1])
        last_move = Movement(last_crane_pos,default_crane_pos)
        last_move.cost = last_cost
        path.append(last_move)
        
        for move in path:

            from_slot = move.get_from_slot()
            to_slot = move.get_to_slot()
            grid_copy.move_container(from_slot, to_slot)
            intermediate_state = copy.deepcopy(grid_copy)
            moves_intermediate_grids.append((move, intermediate_state))

        
        return (moves_intermediate_grids)
    
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

    def sift(self):
        print('Sifting...')
        
        current_ship_grid = self.start_state
        #initialize a 4x24 buffer grid. All slots UNUSED, weight = 0
        buffer_grid = Grid(rows=4, columns=24)
        buffer_grid.setup_grid()

        #get goal_state
        goal_ship_grid = self.get_sift_goal(current_ship_grid)

        #find the shortest path to goal_state. Must update available moves function to consider buffer as an available grid

        # Initialize the open set with the current ship grid
        heapq.heappush(self.open_set, (0, 0, [], current_ship_grid))

        while self.open_set:
            # Pop the state with the lowest cost
            total_cost, path_cost, path, state = heapq.heappop(self.open_set)

            # If the state matches the goal state, return the path
            if state == goal_ship_grid:
                return path

            if state not in self.closed_set:
                self.closed_set.add(state)

            # Generate possible states and moves
            for child_state, move in state.getPossibleStatesMoves(buffer_grid):
                if child_state not in self.closed_set:
                        new_total_cost = total_cost
                        crane_to_start_cost = state.calculate_path_cost(state.crane_position, move.from_slot)
                        move_cost = state.calculate_path_cost(move.from_slot, move.to_slot)
                        new_path_cost = path_cost + crane_to_start_cost + move_cost
                        heuristic_cost = self.sift_heuristic(child_state, goal_ship_grid)
                        new_total_cost += new_path_cost + heuristic_cost
                        move.cost = crane_to_start_cost + move_cost
                        new_path = path + [move]

                        heapq.heappush(self.open_set, (new_total_cost, new_path_cost, new_path, child_state))

        print("No SIFT path found")
        return None
    
    def get_sift_goal(self, grid):

        virtual_grid = copy.deepcopy(grid)
        containers = copy.deepcopy(self.get_containers(virtual_grid))

        print(containers)

        for container in containers: #remove all containers while keeping grid NANs the same
            container_position =  container.get_position()
            row, column = container_position[0], container_position[1]
            virtual_grid.remove_container(row,column)

        heap = []
        midpoint = virtual_grid.columns//2
        left_offset = 1
        right_offset = 0

        left_row = 0
        right_row = 0

        for container in containers:
            container_weight = container.get_weight()
            container_name = container.get_name()
            heapq.heappush(heap, (-container_weight, container)) #push containers to heap, highest weight on top
        for i in range(0, len(heap),):
            heaviest_container = heapq.heappop(heap)[1]
            container_position = heaviest_container.get_position()
            from_slot = virtual_grid.get_slot(container_position[0],container_position[1])

            condition =  i % 2

            if condition == 0: #place container on left half as close as possible to mid point
                column = midpoint - left_offset

                
                if (0 >= column > virtual_grid.columns):
                    left_offset = 1
                    column = midpoint - left_offset
                    left_row += 1
                
                to_slot = virtual_grid.get_slot(left_row, column)

                if to_slot.get_state() == 0:
                    print(f'reached NAN at {left_row}, {column}')
                    left_offset = 1
                    column = midpoint - left_offset
                    left_row += 1
                to_slot = virtual_grid.get_slot(left_row, column)

                
                
                print(f"Move container from position {from_slot.position} to position {left_row}, {column}")
                to_row = to_slot.x
                to_column = to_slot.y
                virtual_grid.add_container(heaviest_container, left_row, column)
                left_offset += 1

            if condition == 1:  # Place container on right half as close as possible to the midpoint
                column = midpoint + right_offset

                if not (0 <= column < virtual_grid.columns):  # Check if column is out of bounds
                    print(f"Reached the edge")
                    right_offset = 1
                    column = midpoint + right_offset
                    right_row += 1

                to_slot = virtual_grid.get_slot(right_row, column)

                if to_slot.get_state() == 0:  # Check if slot is NAN
                    print(f"Reached NAN at {right_row}, {column}")
                    right_offset = 0
                    column = midpoint + right_offset
                    right_row += 1
                to_slot = virtual_grid.get_slot(right_row, column)

                print(f"Move container from position {from_slot.position} to position {right_row}, {column}")
                to_row = to_slot.x
                to_column = to_slot.y
                virtual_grid.add_container(heaviest_container, right_row, column)
                right_offset += 1

        return virtual_grid


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

                current_grid = self.start_state
                path_with_intermediate_grids = self.reconstruct_grids_from_path(current_grid, path)
    
                return path_with_intermediate_grids
            
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
        
    def get_containers(self, grid):
        containers = grid.left_containers.union(grid.right_containers)
        # containers = []
        # for row in range(grid.rows):
        #     for column in range(grid.columns):
        #         container = grid.get_slot(row,column).get_container()

        #         containers.append(container)

        return containers
