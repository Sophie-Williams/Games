""" Adversarial version of Tetris. 
The idea here is to pick the configuration where one of the five pieces yields the worst state evaluation (heuristic) after an optimal placement.
This guarantees that even if the player plays the best game, we are taking that into account and working against him.

The mode works only for the human player in simple and animated mode

By Pralhad Sapre 
"""

from AnimatedTetris import *
from SimpleTetris import *
import TetrisBrain as tb
import sys  

# we have all the things we need in AnimatedTetris [that too derives from Tetris].
class AdversarialTetrisAnimated(AnimatedTetris):
  def __init__(self):
    AnimatedTetris.__init__(self)

  def random_piece(self):
    worst_piece = (sys.maxint, 0)
    optimal_board = self.get_board()

    for i in range(0,len(TetrisGame.PIECES)):
      utility_value = tb.get_best_move(optimal_board, self.get_score(), TetrisGame.PIECES[i])[0] 
      worst_piece = (utility_value, i) if utility_value < worst_piece[0] else worst_piece

    return TetrisGame.rotate_piece(TetrisGame.PIECES[worst_piece[1]], random.randrange(0, 360, 90) )

# we have all the things we need in SimpleTetris [that too derives from Tetris].
class AdversarialTetrisSimple(SimpleTetris):
  def __init__(self):
    SimpleTetris.__init__(self)

  def random_piece(self):
    worst_piece = (sys.maxint, 0)
    optimal_board = self.get_board()

    for i in range(0,len(TetrisGame.PIECES)):  
      utility_value = tb.get_best_move(optimal_board, self.get_score(), TetrisGame.PIECES[i])[0] 
      worst_piece = (utility_value, i) if utility_value < worst_piece[0] else worst_piece
      
    return TetrisGame.rotate_piece(TetrisGame.PIECES[worst_piece[1]], random.randrange(0, 360, 90) ) 
