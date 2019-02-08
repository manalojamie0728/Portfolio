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

Matrix Generation (Prototype):
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

Matrix Generation (New):
        Given a matrix with 4 rows (mathematical operations) and k-columns,
        fill the rule matrix according to the 4x4 magic square.

Math Operations:
    0: Addition; Add current digit with the digit's position
    1: Subtraction; Subtract current digit by the digit's position
    2: Multiplication; Multiply current digit by the digit's position
    3: Exponentiation; Exponentiate current digit to the digit's position

    Ex: Let n be the digit value, i be the digit position. n+i, n-i, n*i,
        and n**(i%10) are the four operations, respectively. Modulo by the
        number of digits plus 1, k+1, if necessary. If first digit is 0, add 1.

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
from master import Master
from solver import Solver

k = 5
M = Master(k)

# START GAME HERE
n = M.generate_goal()
while (M.check_goal(n)):
    n = M.generate_number()

name = raw_input("Tell me your name: ")
print("To get out, you must reach Position "+str(M.generate_goal()))
while (not M.check_goal(n)):
    print("\n================ ONE-WAY WOODS (OWW) ================")
    print(name+", what do you want to do?\nACT:\n[U] Go Up/Forward\n[D] Go Down/Back\n[L] Go Left\n[R] Go Right\n[-] Wait\n\nOTHER:\n[S] Show Me The Way\n[E] Exhaust Nodes\n[Q] Quit\n")
    print("Current Position: "+str(n))
    i = raw_input("Choice: ")
    if (i.upper() == 'Q'):
        break
    elif (i.upper() == 'S'):
        print("Yuu giving up? Ha! Weak...")
        Solver(n, k).solve(True)
        break
    elif (i.upper() == 'E'):
        Solver(n, k).exhaust_nodes()
        break
    else:
        n = M.move(i.upper(), n)

if M.check_goal(n):
    print("\nCurrent Position: "+str(n))
    print("************ CONGRATULATIONS! YOU GOT OUT ALIVE! ************")
else:
    print("\nGood night...")

"""
OBSERVATIONS:
- Interesting... So the columns repeat after 4 columns. Which means columns
  1, 5, 9, etc. have the same values. In general, if there i rows and j
  columns, then j, i+j, 2i+j, ... have the same column compositions.
- Some nodes are two-way; that is, they are inverses of each other. Most nodes
  are one-way as expected of One-Way Woods.

"""
