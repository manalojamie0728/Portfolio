# GRAPH FOR ONE-WAY WOODS SOLVER
import numpy as np
import random
from master import Master

class Graph:
    def __init__(self, k):
        # Pointers to root, and solution nodes; initially None
        self.root = None
        self.solution = None
        self.M = Master(k)

        # List of values already visited and discovered
        self.visited = []
        self.bfs_disc_val = []

        # Queue of nodes to visit in BFS
        self.bfs_queue = []

    def init_root(self, val):
        N = Node(val)
        self.root = N

    def bfs_traversal(self, N):
        # Check moves in the ff. order: U, R, D, L, Wait (-)
        directions = ['U', 'R', 'D', 'L', '-']
        for d in directions:
            n = self.M.move(d, N.val)
            if (n not in self.visited) and (n not in self.bfs_disc_val):
                if d == 'U':
                    N.up = Node(n, N.path+d)
                    self.bfs_queue.append(N.up)
                    if self.M.check_goal(N.up.val):
                        N = N.up
                        break
                elif d == 'R':
                    N.right = Node(n, N.path+d)
                    self.bfs_queue.append(N.right)
                    if self.M.check_goal(N.right.val):
                        N = N.right
                        break
                elif d == 'D':
                    N.down = Node(n, N.path+d)
                    self.bfs_queue.append(N.down)
                    if self.M.check_goal(N.down.val):
                        N = N.down
                        break
                elif d == 'L':
                    N.left = Node(n, N.path+d)
                    self.bfs_queue.append(N.left)
                    if self.M.check_goal(N.left.val):
                        N = N.left
                        break
                elif d == '-':
                    N.wait = Node(n, N.path+d)
                    self.bfs_queue.append(N.wait)
                    if self.M.check_goal(N.wait.val):
                        N = N.wait
                        break
                self.bfs_disc_val.append(n)
        self.visited.append(N.val)
        
        if self.M.check_goal(N.val):
            self.solution = N
            return True
        return False

    def bfs_driver(self):
        # Enqueue root as initial point
        self.bfs_queue.append(self.root)
        self.bfs_disc_val.append(self.root.val)
        
        while len(self.bfs_queue) > 0:
            if(self.bfs_traversal(self.bfs_queue.pop(0))):
                break
        return self.solution

class Node:
    def __init__(self, val, path=""):
        # Determines values of resulting actions
        self.up = None
        self.right = None
        self.down = None
        self.left = None
        self.wait = None

        # Current Node Value and Path
        self.val = val
        self.path = path
