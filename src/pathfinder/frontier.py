import heapq
# structure to keep the grids for search algorithm 

class Frontier:
    def __init__(self):
        self.heap = []
        self.states = set()
        self.current_max_size = 0 # For testing purposes
        
    def insert(self, node):
        if node not in self.states:
            heapq.heappush(self.heap, node)
            self.states.add(node)
            if len(self.heap) > self.current_max_size:
                self.current_max_size = len(self.heap)
    
    def pop(self):
        if self.heap:
            node = heapq.heappop(self.heap)
            self.states.remove(node)
            return node
        return None
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def max_queue_size(self):
        return self.current_max_size
    
    def contains_state(self, state):
        return state in self.states
        
        