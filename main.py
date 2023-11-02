import numpy as np
import time
from queue import Queue

class Sudoku:
    def __init__(self, board, even_list):
        self.board = np.array(board)
        self.visited = np.zeros(self.board.shape, dtype=bool) #for mrv heuristic
        self.domain_list = [[set() for j in range(9)] for i in range(9)]
        self.removed_domain = [[[] for j in range(9)] for i in range(9)] #for forward check 
        self.filled = 0
        self.CELL_COUNT = 81
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if (i, j) in even_list:
                        self.domain_list[i][j] = {val for val in range(2, 10, 2)}
                    else:
                        self.domain_list[i][j] = {val for val in range(1, 10)}
                else:
                    self.filled += 1
                    self.domain_list[i][j] = set()
                    self.forward_check(i, j, board[i][j])

        self.apply_arc_consistency()


    def get_next_position(self, line, col): #Minimum remaining values
        next_line, next_col = 0, 0
        minimum_remaining_values = 10

        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0 or self.visited[i][j] is True:
                    continue
                domain = self.domain_list[i][j] - set(self.removed_domain[i][j])
                if len(domain) < minimum_remaining_values:
                    minimum_remaining_values = len(domain)
                    next_line, next_col = i, j

        return next_line, next_col


    def print_solution(self):
        print(self.board)
        print(f"Time: {time.time() - start_time} seconds")


    def forward_check(self, lin, col, val, revert=False):
        #revert - true daca aplic forward check, fals daca trebuie sa restitui schimbarile
        change_removed_domain = lambda i, j: self.removed_domain[i][j].append(val) if self.board[i][j] == 0 else None
        if revert is True:
            change_removed_domain = lambda i, j: self.removed_domain[i][j].remove(val) if self.board[i][j] == 0 else None

        for j in range(9):
            if j == col:
                continue
            change_removed_domain(lin, j)

        for i in range(9):
            if i == lin:
                continue 
            change_removed_domain(i, col)
                    
        for i in range(lin // 3 * 3, lin // 3 * 3 + 3):
            for j in range(col // 3 * 3, col // 3 * 3 + 3):
                if i == lin or j == col: #am mers deja o data pe linii si coloane
                    continue 
                change_removed_domain(i, j)


    def get_neighbours(self, i, j):
        neighbours = []
        #adaug vecinii pe linii si coloane
        for k in range(9):
            if (i, j) != (i, k) and self.board[i][k] == 0:
                neighbours.append((i, k))
            if (k, j) != (i, j) and self.board[k][j] == 0:
                neighbours.append((k, j))
        #adaug vecinii din patrat
        for square_i in range(i // 3 * 3, i // 3 * 3 + 3):
            for square_j in range(j // 3 * 3, j // 3 * 3 + 3):
                if i == square_i or j == square_j or self.board[square_i][square_j] != 0:
                    continue 
                neighbours.append((square_i, square_j))
        return neighbours


    def remove_inconsistent_values(self, cell_0, cell_1):
        removed = set()

        domain_0 = self.domain_list[cell_0[0]][cell_0[1]] - set(self.removed_domain[cell_0[0]][cell_0[1]])
        for val_0 in domain_0:
            is_removed = True
            domain_1 = self.domain_list[cell_1[0]][cell_1[1]] - set(self.removed_domain[cell_1[0]][cell_1[1]])
            for val_1 in domain_1:
                if val_1 != val_0: 
                    is_removed = False
            if is_removed:
                removed.add(val_0)

        self.domain_list[cell_0[0]][cell_0[1]] = self.domain_list[cell_0[0]][cell_0[1]] - removed
        
        return len(removed) > 0


    def apply_arc_consistency(self):
        #initializez coada cu arce
        q = Queue()
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    continue
                for neighbour in self.get_neighbours(i, j):
                    q.put(((i, j), neighbour))
                
        while not q.empty():
            cell_0, cell_1 = q.get()
            if self.remove_inconsistent_values(cell_0, cell_1):
                for neighbour in self.get_neighbours(cell_0[0], cell_0[1]):
                    q.put((neighbour, cell_0))



    def solve(self, lin, col):
        forward_check_domain = self.domain_list[lin][col] - set(self.removed_domain[lin][col])

        for val in forward_check_domain:
            if Validator.is_valid_move(self.board, lin, col, val):
                self.board[lin][col] = val
                self.filled += 1
                self.visited[lin][col] = True
                if self.filled == self.CELL_COUNT:
                    self.print_solution()
                    exit(0)

                self.forward_check(lin, col, val)
                next_line, next_col = self.get_next_position(lin, col)

                self.solve(next_line, next_col)

                self.board[lin][col] = 0
                self.filled -= 1
                self.visited[lin][col] = False
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

other_matrix = [
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
lab_matrix = [
    [8, 4, 0, 0, 5, 0, 0, 0, 0],
    [3, 0, 0, 6, 0, 8, 0, 4, 0],
    [0, 0, 0, 4, 0, 9, 0, 0, 0],
    [0, 2, 3, 0, 0, 0, 9, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 9, 8, 0, 0, 0, 1, 6, 0],
    [0, 0, 0, 5, 0, 3, 0, 0, 0],
    [0, 3, 0, 1, 0, 6, 0, 0, 7],
    [0, 0, 0, 0, 2, 0, 0, 1, 3]
]
even_list = [
    (0, 6),
    (2, 2), (2, 8),
    (3, 4),
    (4, 3), (4, 5),
    (5, 4),
    (6, 0), (6, 6),
    (8, 2)
]

s = Sudoku(lab_matrix, even_list)
line, col = s.get_next_position(0, -1)

start_time = time.time()
s.solve(line, col)