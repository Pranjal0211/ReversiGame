import os, copy
import numpy as np

# CONSTANTS
dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
diry = [-1, -1, -1, 0, 0, 1, 1, 1]

BACKGROUND_COLOR = "\x1b[41;1m"  
RESET_COLOR = "\x1b[0m"
SCORESP_COLOR = "\x1b[1;32;42m"
SCORESA_COLOR = "\x1b[1;36;46m"
BLACK=" ⚫️ "
WHITE=" ⚪️ "


class ReversiGame:
    """A n X n variant game also know as othello"""
    
    def __init__(self, n): # initialize board and players initial piece position
        self.n = n
        self.depth = n
        self.board = [['    ' for i in range(self.n)] for i in range(self.n)]
        z = (self.n - 2) // 2
        self.board[z][z] = WHITE
        self.board[self.n - 1 - z][z] = BLACK        
        self.board[z][self.n - 1 - z] = BLACK
        self.board[self.n - 1 - z][self.n - 1 - z] = WHITE
        self.minEvalBoard = -np.inf
        self.maxEvalBoard = np.inf

    def printBoard(self): # UI to render on terminal
        b = self.board
        for i in range(self.n):
            if(i == 0):
                print('  ', end = '')
            print(f'  {i}  ', end = '')
        print()
        for i in range(self.n):
            print(' ', end = '')
            for j in range(self.n):
                print(f'{BACKGROUND_COLOR}┼────', end = '')
            print(f'┼{RESET_COLOR}')
            print(f'{i}', end = '')
            for j in range(self.n):
                print(f'{BACKGROUND_COLOR}│{b[i][j]}', end = '')
            print(f'│{RESET_COLOR}{i}')
        print(' ', end = '')
        for j in range(self.n):
                print(f'{BACKGROUND_COLOR}┼────', end = '')
            
        print(f'┼{RESET_COLOR}')
        for i in range(self.n):
            if(i == 0):
                print('  ', end = '')
            print(f'  {i}  ', end = '')
        print()

    def makeMove(self, board, x, y, player): 
        totctr = 0 # total number of opponent pieces taken
        board[y][x] = player
        for d in range(8): 
            ctr = 0
            for i in range(self.n):
                dx = x + dirx[d] * (i + 1)
                dy = y + diry[d] * (i + 1)
                if dx < 0 or dx > self.n - 1 or dy < 0 or dy > self.n - 1:
                    ctr = 0; break
                elif board[dy][dx] == player:
                    break
                elif board[dy][dx] == '    ':
                    ctr = 0; break
                else:
                    ctr += 1
            for i in range(ctr):
                dx = x + dirx[d] * (i + 1)
                dy = y + diry[d] * (i + 1)
                board[dy][dx] = player
            totctr += ctr
        return (board, totctr)

    def validMove(self, board, x, y, player): # check if move is valid
        if x < 0 or x > self.n - 1 or y < 0 or y > self.n - 1:
            return False
        if board[y][x] != '    ':
            return False
        (boardTemp, totctr) = self.makeMove(copy.deepcopy(board), x, y, player)
        if totctr == 0:
            return False
        return True
    
    def evalBoard(self, board, player): # works as a utility
        tot = 0
        for y in range(self.n):
            for x in range(self.n):
                if board[y][x] == player:
                    tot += 1
        return tot
    
    def isTerminalNode(self, board, player): # find if this is last valid move
        for y in range(self.n):
            for x in range(self.n):
                if self.validMove(board, x, y, player):
                    return False
        return True
    
    def alphaBetaSearch(self, board, player, depth, alpha, beta, maximizingPlayer): # Algo for AI player
        if depth == 0 or self.isTerminalNode(board, player):
            return self.evalBoard(board, player)
        if maximizingPlayer:
            v = self.minEvalBoard
            for y in range(self.n):
                for x in range(self.n):
                    if self.validMove(board, x, y, player):
                        (boardTemp, totctr) = self.makeMove(copy.deepcopy(board), x, y, player)
                        v = max(v, self.alphaBetaSearch(boardTemp, player, depth - 1, alpha, beta, False))
                        alpha = max(alpha, v)
                        if beta <= alpha:
                            break # beta cut-off
            return v
        else: # minimizingPlayer
            v = self.maxEvalBoard
            for y in range(self.n):
                for x in range(self.n):
                    if self.validMove(board, x, y, player):
                        (boardTemp, totctr) = self.makeMove(copy.deepcopy(board), x, y, player)
                        v = min(v, self.alphaBetaSearch(boardTemp, player, depth - 1, alpha, beta, True))
                        beta = min(beta, v)
                        if beta <= alpha:
                            break # alpha cut-off
            return v

    def bestMove(self, board, player): # helper function for Algo
        maxPoints = 0
        mx = -1; my = -1
        for y in range(self.n):
            for x in range(self.n):
                if self.validMove(board, x, y, player):
                    # (boardTemp, totctr) = makeMove(copy.deepcopy(board), x, y, player)
                    points = self.alphaBetaSearch(board, player, self.depth, self.minEvalBoard, self.maxEvalBoard, True)
                    
                    if points > maxPoints:
                        maxPoints = points
                        mx = x; my = y
        return (mx, my)




