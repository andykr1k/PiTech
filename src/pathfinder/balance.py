from models.grid_balance import  GridState
from pathfinder.frontier import Frontier

# structure for search
class Balance_Problem:
    
        
    def __init__(self, initial_gridstate):
   
        self.initial_gridstate = initial_gridstate
        self.frontier = Frontier()  # Frontier object for holding the search nodes
        self.node_expanded_count = 0  # Testing pruposes
        
    def solve(self):
        max_iter = 200
        explored_set = set()
        root_state = self.initial_gridstate
        self.frontier.insert(root_state)
        
        while not self.frontier.is_empty():
            current_state = self.frontier.pop()
            #print(f"current state {current_state} /n----------------------")
            #print(current_state.get_weight())
            if current_state.isBalanced():
                print("========\nBalanced\n========")
                #print(current_state)
                print(f"Total states expanded:{self.node_expanded_count}")
                #current_state.print_path()
                return current_state
            explored_set.add(current_state)
            children_states = current_state.expand()
            self.node_expanded_count += len(children_states)
            print(f"expanding...{len(children_states)} states")
            print(f"Total states explored: {self.node_expanded_count}")
            if self.node_expanded_count > max_iter:
                print("Erro, Can not be balances")
                # Go to SIFT
                return 0
            #for c in children_states:
                #print(c.cost)
            for child in children_states:
                if child not in explored_set and not self.frontier.contains_state(child):
                    self.frontier.insert(child)
                    
                
            
            
    
        
    
