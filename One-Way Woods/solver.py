# SOLVER FOR ONE-WAY WOODS (GENERAL)
import numpy as np
import time
from master import Master
from graph import Graph

class Solver:
    def __init__(self, val, k):
        self.k = k
        self.val = val

    def solve(self, show_sol):
        self.graph = Graph(self.k)
        self.graph.init_root(self.val)
        N = self.graph.bfs_driver() # For CSV recording purposes...

        if show_sol:
            print "\n***********************"
            print self.val, N.path, N.val, "\n***********************"

    def exhaust_nodes(self):
        print "Running..."
        t0 = time.time()
        self.val = 10**(self.k-1)
        for i in range(self.k*((self.k+1)**(self.k-1))):
            self.solve(False)
            self.val = self.base_add(self.val)
        print "Done! Time taken to exhaust:", time.time()-t0, "s"

    def base_add(self, n):
        # Perform a base-(k+1) increment, provided k < 9
        n += 1
        n = str(n)
        for i in range(self.k-1, 0, -1):
            if int(n[i]) == self.k+1:
                n = n[:i-1]+str(int(n[i-1])+1)+'0'+n[i+1:]
        return int(n)

#S = Solver(11111, 5)
#S.exhaust_nodes()
