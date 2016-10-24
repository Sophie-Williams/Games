""" 
Tetris Questions:
1. A description of how you formulated the search problem, including precisely defining the state
space, the successor function, the edge weights, and any heuristics you designed
    State: 10X20 matrix structure representing the board

    Successor function:  
    Generates all possible combinations using both the current piece and future piece placable on the board inclusive of their rotations.

    Edge weight: 
    Edge weight is uniform. And in this problem in general is immaterial

    Heuristics: 
    It is weighted linear sum of maximum height on the board, number of lines clearable, number of holes in the structure, uneven surface and blockades

2. A brief description of how your search algorithm works
    Computer Player
    1. For a given current piece and next piece all the possible states are generated
    2. Then Heuristics is calculated for each board states [with both pieces placed]
    3. Out of all the calculated Heuristics the best move is chosen

    Adversarial
    1. With the current board state all possible states are generated for the every allowed piece
    2. Heuristics is calculated for the generated board states
    3. Out of all the calculated Heuristics the least weighted state is chosen and it corresponding piece would be the current piece

3. Discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made
    Simplification:
    1. Instead of using a priority queue, we have used a single variable to hold best move. This yielded significant space and time optimization

    Design Decisions:
    1. Making use of the next piece as a part of the total heuristic function value


Improvements:
You could try to learn the probability distribution of the pieces from their observation and even estimate the population from which the piece is randomly drawn.
But given the fact that the piece is drawn randomly from this population makes it hard to predict the next step and win in the game [maximize the number of lines]

"""


from AnimatedTetris import *
from SimpleTetris import *
from AdversarialTetris import *
import TetrisBrain as tb
from kbinput import *
import time, sys
import random

class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
    
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. tetris is an object that lets you inspect the board, e.g.:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    
    def get_moves(self, tetris):
        # algorithm for picking the best placement of the given piece with one level lookahead
        return tb.get_best_move(tetris.get_board(), tetris.get_score(), tetris.get_piece()[0], tetris=tetris, recurse=True)[1]        
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, tetris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            for move in tb.get_best_move(tetris.get_board(), tetris.get_score(), tetris.get_piece()[0], tetris=tetris, recurse=True)[1]:
                if move == 'b':
                    tetris.left()
                elif move == 'm':
                    tetris.right()
                elif move == 'n':
                    tetris.rotate()
            tetris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]
adversarial = False
if len(sys.argv) == 4:    
    if sys.argv[3] == 'adversarial' and sys.argv[1] == 'human':
        adversarial = True
    else:
        print "4th option name should be [adversarial] with [animated/simple] version and [human] player"
        sys.exit()
try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris() if not adversarial else AdversarialTetrisSimple()
    elif interface_opt == "animated":    
        tetris = AnimatedTetris() if not adversarial else AdversarialTetrisAnimated()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s