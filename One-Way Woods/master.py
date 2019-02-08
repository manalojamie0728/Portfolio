# MASTER CONTROL FOR ONE-WAY WOODS
import numpy as np
import random

class Master:
    def __init__(self, k): # k is how many digits needed; 2 <= k <= 9
        self.k = k
        self.directions = ['U', 'R', 'D', 'L']
        self.rules = np.empty([4, self.k], dtype=str)
        self.goal = self.generate_goal()

        self.build_rules()

    """
    def build_rules0(self):
        # Fill the matrix in this order: U, D, R, L
        row, col = 0, 0 # row and col are anchors
        for d in range(4): # d is directional number
            row, col = d, 0
            while col < self.k:
                if d == 0:
                    self.rules[row, col] = 'U'
                    col += 1
                    row = (row+1) % 4   # Modulo for wrap-around

                elif d == 1:
                    self.rules[row, col] = 'D'
                    col += 1
                    row = (row+col+1) % 4
                    if col >= self.k:
                        break
                    while self.rules[row, col] in self.directions:
                        row = (row+1) % 4

                elif d == 2:
                    self.rules[row, col] = 'R'
                    col += 1
                    row = (row+2*col-1) % 4
                    if col >= self.k:
                        break
                    while self.rules[row, col] in self.directions:
                        row = (row+1) % 4

                elif d == 3:
                    self.rules[row, col] = 'L'
                    col += 1
                    row = (row+1) % 4
                    if col >= self.k:
                        break
                    while self.rules[row, col] in self.directions:
                        row = (row+1) % 4
    """

    def build_rules(self):
        # Fill the matrix in this order: U, R, D, L
        row, col = 0, 0 # row and col are anchors
        for d in range(4): # d is directional number
            row, col = d, 0
            while col < self.k:
                if d == 0:
                    self.rules[row, col] = 'U'
                    col += 1
                    row = (row+(4-col)) % 4   # Modulo for wrap-around

                elif d == 1:
                    self.rules[row, col] = 'R'
                    col += 1
                    row = (row+(col)) % 4

                elif d == 2:
                    self.rules[row, col] = 'D'
                    col += 1
                    row = (row+(4-col)) % 4

                elif d == 3:
                    self.rules[row, col] = 'L'
                    col += 1
                    row = (row+(col)) % 4

                if col%4 == 0:
                    row = (row+2) % 4

    def generate_number(self):
        n = ''
        for i in range(self.k):
            n += str(random.randint(1,self.k))
        return int(n)

    def generate_goal(self):
        n = ''
        for i in range(1,self.k+1):
            n += str(i)
        return int(n)

    def check_goal(self, n):
        if n == self.goal:
            return True
        return False

    def parse_direction(self, d): # d is a direction: U, D, R, L
        d_dict = {'U': '1423',
                  'R': '2314',
                  'D': '3241',
                  'L': '4132'} # Based on the current set of rules
        p = '' # Parse string to determine operation per digit
        for i in range(self.k):
            p += d_dict[d][i%4]
        return p

    def move(self, d, n): # d is a direction or Wait, n is the current position
        if d == '-': # If Wait...
            e = 1 # Marker to last digit; for modulo
            while n%(10**e) == 0:
                e += 1
            n = n//(10**e) + (n%(10**e))*(10**(self.k-e)) # Bit shift
        elif d in self.directions:
            p = self.parse_direction(d)
            n_str = str(n)
            n = ''
            for i in range(self.k): # Iterate through the number's digits
                if p[i] == '1': # Addition
                     digit = (int(n_str[i])+(i+1))%(self.k+1)
                elif p[i] == '2': # Subtraction
                    digit = (int(n_str[i])-(i+1))%(self.k+1)
                elif p[i] == '3': # Multiplication
                    digit = (int(n_str[i])*(i+1))%(self.k+1)
                elif p[i] == '4': # Exponentiation
                    digit = (int(n_str[i])**((i+1)%10))%(self.k+1)
                if i == 0 and digit == 0:
                    digit += 1
                n += str(digit)
            n = int(n)
        else:
            print("\nERROR! Input not recognized.\n")
        return n
