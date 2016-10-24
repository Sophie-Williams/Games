import sys
import random
from SimpleTetris import *

def printboard(board):
    for line in board:
        print line

def board_utility(board):
    max_height = -100
    gaps = 0.0
    blockade = 0    
    heights = []

    # check for gaps
    for c in range(0,len(board[0])):    
        count = False    
        last_blockade = 0
        for r in range(0,len(board)):
            if board[r][c] != ' ':
                if not count:
                    count = True
                    max_height = (len(board) - r) if (len(board) - r) > max_height else max_height
                    heights.append(len(board) - r)
                if last_blockade == 0:
                    last_blockade = r

            if board[r][c] == ' ' and count:
                if last_blockade != 0:
                    blockade += r-last_blockade
                    last_blockade = 0
                gaps += 1

        if not count:
            heights.append(0)

    # check for uneven surface
    uneven = 0.0
    for c in range(0,len(board[0])-1,1):
        uneven += abs(heights[c] - heights[c+1])

    lines = sum([1 if ' ' not in row else 0 for row in board])
    avg_height = sum(heights)*1.0/len(heights)
    # utility = avg_height*(-0.510066) + lines*(0.760666) + gaps*(-0.35663) + uneven*(-0.184433) 

    utility = max_height*(-0.7) + lines*5.0 + gaps*(-1.4) + uneven*(-0.7) + blockade*(-0.4)
    # print utility
    return utility

def get_best_move(old_board, score, piece, tetris=None, recurse=False):
    rotations = {}
    rotations_list = []
    for i in range(0, 360, 90):
        val = TetrisGame.rotate_piece(piece, i)
        if str(val) not in rotations:
            rotations[str(val)] = val
            rotations_list.append(val)

    bestmove = (-sys.maxint, old_board)
    for r in range(0,len(rotations.values())):
        piece = rotations_list[r]
        for col in range(0, 10-len(piece[0])+1):       
            for row in range(0, 20): 
                collided = TetrisGame.check_collision((old_board, score), piece, row, col)            
                if collided or row == 20-len(piece):
                    board = TetrisGame.place_piece((old_board, score), piece, row-1 if collided else row, col)[0]
                    # printboard(board)
                    score = board_utility(board)
                    if recurse:
                        score = get_best_move(board, score, tetris.get_next_piece())[0]
                        bestmove = (score, "n"*r + abs(tetris.col-col)*("b" if (tetris.col-col) > 0 else "m"), board) if score >= bestmove[0] else bestmove
                    else:
                        bestmove = (score, board) if score >= bestmove[0] else bestmove
                    break
    
    return bestmove