import numpy as np


class Sudoku:
    def __init__(self, board, even_list):
        self.board = np.array(board)
        self.domain_list = [[[] for j in range(9)] for i in range(9)]
        self.filled = 0
        self.CELL_COUNT = 81
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if (i, j) in even_list:
                        self.domain_list[i][j] = [val for val in range(2, 10, 2)]
                    else:
                        self.domain_list[i][j] = [val for val in range(1, 10)]
                else:
                    self.filled += 1
                    self.domain_list[i][j] = []
    def get_next_position(self, line, col):
        #verific daca e liber
        for j in range(col + 1, 9):
            if self.board[line][j] == 0:
                return line, j

        for i in range(line + 1, 9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return 0, 0

    def print_solution(self):
        print(self.board)

    def forward_check(self, lin, col, val, revert=False):
        for j in range(9):
            if j == col:
                continue
            if not revert: 
                if val in self.domain_list[lin][j]:
                    self.domain_list[lin][j].remove(val)
            else:
                if Validator.is_valid_move(self.board, lin, j, val):
                    self.domain_list[lin][j].append(val)
        for i in range(9):
            if i == lin:
                continue 
            if not revert:
                if val in self.domain_list[i][col]:
                    self.domain_list[i][col].remove(val)
            else:
                if Validator.is_valid_move(self.board, i, col, val):
                    self.domain_list[i][col].append(val)
                    
        for i in range(line // 3 * 3, line // 3 * 3 + 3):
            for j in range(col // 3 * 3, col // 3 * 3 + 3):
                if i == lin and j == col:
                    continue 
                if not revert:
                    if val in self.domain_list[i][j]:
                        self.domain_list[i][j].remove(val)
                else:
                    if Validator.is_valid_move(self.board, i, j, val):
                        self.domain_list[i][j].append(val)


    def solve(self, lin, col):
        for val in self.domain_list[lin][col]:
            if Validator.is_valid_move(self.board, lin, col, val):
                self.board[lin][col]=val
                self.filled += 1
                if self.filled == self.CELL_COUNT:
                    self.print_solution()
                    exit(0)

                self.forward_check(lin, col, val)
                next_line, next_col = self.get_next_position(lin, col)

                self.solve(next_line, next_col)

                self.board[lin][col] = 0
                self.filled -= 1
                self.forward_check(lin, col, val, revert=True)


class Validator:
    def is_valid_line(board, line, val):
        return val not in board[line]

    def is_valid_column(board, col, val):
        return val not in board[0:9 , col]

    def is_valid_square(board, line, col, val):
        return val not in board[line // 3 * 3: line // 3 * 3 + 3, col // 3 * 3: col // 3 * 3 + 3]

    def is_valid_move(board, line, col, val):
        return Validator.is_valid_line(board,line,val) and Validator.is_valid_column(board,col,val) and Validator.is_valid_square(board,line,col,val)


solvable_sudoku = [
    [5, 0, 0, 0, 7, 0, 0, 0, 0],
    [6, 7, 0, 1, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 0],
    [4, 0, 0, 8, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
sudoku_board = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 0, 2, 1, 9, 5, 3, 0, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [0, 0, 0, 5, 3, 7, 2, 8, 4],
    [0, 0, 0, 4, 1, 9, 6, 3, 5],
    [0, 0, 0, 2, 8, 6, 1, 7, 9]
]
even_list = []
s = Sudoku(solvable_sudoku, even_list)
line, col = s.get_next_position(0, -1)

s.solve(line, col)