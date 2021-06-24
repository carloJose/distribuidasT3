. 
class Node:

    def __init__(self):
        self.neighbors = set()
        self.n_neighbors = 0

    @check_start
    def event(self):
        pass
    
    def check_start(self,function):
        if self.n_neighbors == len(self.neighbors):
            function()