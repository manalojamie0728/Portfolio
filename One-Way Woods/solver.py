# SOLVER FOR ONE-WAY WOODS (GENERAL)
import numpy as np
import random
from master import Master
from graph import Graph

class Solver:
    def __init__(self, val, k):
        self.graph = Graph(k)
        self.val = val

    def solve(self):
        self.graph.init_root(self.val)
        self.graph.bfs_driver()
