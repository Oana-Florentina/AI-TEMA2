import numpy as np


class Sudoku:
    def __init__(self, board, even_list):
        self.board = np.array(board)
        self.domain_list = [[[] for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if (i, j) in even_list:
                        self.domain_list[i][j] = [val for val in range(2, 10, 2)]
                    else:
                        self.domain_list[i][j] = [val for val in range(1, 10)]
                else:
                    self.domain_list[i][j] = []

        

sudoku_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
even_list = [(0, 2), (0, 3)]
s = Sudoku(sudoku_puzzle, even_list)