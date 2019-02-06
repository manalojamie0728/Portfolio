# ONE-WAY WOODS GAME - Where Waiting Gets You Moving

"""
Goal:   Given a random number with k-digits (initial digit values from 1 to k),
        get to the goal number, 123...(k-1)k in the fewest moves possible.
        For example, 9-digit OWW has a goal of 123456789 and a random
        starting number from 111111111 (though 100000000 is the lowest
        possible value) to 999999999.

Rules:  The player can move in five different ways, four of which are
        directional. The fifth is "Wait."

        DIRECTIONAL: Based on the generated 4xk matrix. Each direction
                    has a unique mathematical operation for each digit.
                    Operations are addition, subtraction, multiplication,
                    and exponentiation. Modulo k+1 is used is necessary.
        WAIT:       Right circular bit-shift. For example, the current
                    position/number is 41521. Waiting results in 14152,
                    21415, etc. If 0 is the last digit, keep shifting
                    until the first digit is non-zero.

Matrix Generation:
        Given a matrix with 4 rows (mathematical operations) and k-columns,
        fill the rule matrix as follows (in order):

        'U':    Start from [0,0]. Move diagonally. Wrap around to first row
                if current digit i is divisible by 4.
        'D':    Start from [1,0]. At the i-th digit, move i spaces downward
                and fill in the blank (wrap around if necessary). If slot
                is occupied, move downward until space is blank.
        'R':    Start from [2,0]. At i-th digit, move (2i-1) spaces downward
                and fill in the blank (wrap around if necessary). If slot
                is occupied, move downward until space is blank.
        'L':    Start from [3,0]. Fill in the remaining blanks.

Math Operations:
    0: Addition; Add current digit with the digit's position
    1: Subtraction; Subtract current digit by the digit's position
    2: Multiplication; Multiply current digit by the digit's position
    3: Exponentiation; Exponentiate current digit to the digit's position

    Ex: Let n be the digit value, i be the digit position. n+i, n-i, n*i,
        and n**i are the four operations, respectively. Modulo by the number
        of digits plus 1, k+1, if necessary. If first digit is 0, add 1.

Methods:
    build_rules(): Build the operation/rule matrix based on the number of digits
        used in the game.
    generate_number(): Generate the starting number (n). May repeat if generated
        number equals the goal number.
    generate_goal(): Generate the goal number (n) based on the number of digits used
        in the game.
    check_goal(n): Checks if the current position or number (n) matches the
        goal number.
    parse_direction(d): Generates an instruction string (p) based on the given
        direction (d) and the rule matrix.
    move(d,n): Processes user input (d) and manipulates the current position or
        number (n) accordingly.
"""

import numpy as np
import random

class Master:
    def __init__(self, k): # k is how many digits needed; 2 <= k <= 9
        self.k = k
        self.directions = ['U', 'D', 'R', 'L']
        self.rules = np.empty([4, self.k], dtype=str)
        self.goal = self.generate_goal()

        self.build_rules()

    def build_rules(self):
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
        d_dict = {'U': '1234',
                  'D': '2441',
                  'R': '3112',
                  'L': '4323'} # Based on the current set of rules
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
                    digit = (int(n_str[i])**(i+1))%(self.k+1)
                if i == 0 and digit == 0:
                    digit += 1
                n += str(digit)
            n = int(n)
        return n

M = Master(5)

"""
OBSERVATIONS:
- Interesting... So the columns repeat after 4 columns. Which means columns
  1, 5, 9, etc. have the same values. In general, if there i rows and j
  columns, then j, i+j, 2i+j, ... have the same column compositions.
- Some nodes are two-way; that is, they are inverses of each other. Most nodes
  are one-way as expected of One-Way Woods

"""
