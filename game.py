#!/usr/bin/env python3
import random
from itertools import groupby, chain

NONE = '.'
RED = 'R'
YELLOW = 'Y'

def diagonalsPos(matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if 0 <= i < cols and 0 <= j < rows]

def diagonalsNeg(matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if 0 <= i < cols and 0 <= j < rows]

class Game:
    def __init__(self, cols=7, rows=6, requiredToWin=4):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin
        self.board = [[NONE] * rows for _ in range(cols)]

    def insert(self, column, color):
        """Insert the color in the given column."""
        c = self.board[column]
        if c[0] != NONE:
            raise Exception('Column is full')

        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color

        self.checkForWin()

    def checkForWin(self):
        """Check the current board for a winner."""
        w = self.getWinner()
        if w:
            self.printBoard()
            raise Exception(w + ' won!')

    def getWinner(self):
        """Get the winner on the current board."""
        lines = (
            self.board,  # columns
            zip(*self.board),  # rows
            diagonalsPos(self.board, self.cols, self.rows),  # positive diagonals
            diagonalsNeg(self.board, self.cols, self.rows)  # negative diagonals
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != NONE and len(list(group)) >= self.win:
                    return color

    def printBoard(self):
        """Print the board."""
        print('  '.join(map(str, range(self.cols))))
        for y in range(self.rows):
            print('  '.join(str(self.board[x][y]) for x in range(self.cols)))
        print()

    def computerMove(self, color):
        """Generate a computer move."""
        # Choose a random column initially
        column = random.randint(0, self.cols - 1)

        # Look for the first available column starting from random
        for col in range(column, self.cols):
            if self.board[col][0] == NONE:
                self.insert(col, color)
                return

        # If no column is available, choose a random column
        while True:
            col = random.randint(0, self.cols - 1)
            if self.board[col][0] == NONE:
                self.insert(col, color)
                return


if __name__ == '__main__':
    g = Game()
    turn = RED
    while True:
        g.printBoard()

        if turn == RED:
            row = input('{}\'s turn (0-{}): '.format('Red', g.cols - 1))
            g.insert(int(row), turn)
        else:
            print('Computer\'s turn (Yellow): ')
            g.computerMove(turn)

        # Switch turns
        turn = YELLOW if turn == RED else RED
