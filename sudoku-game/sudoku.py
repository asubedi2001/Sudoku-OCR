class Sudoku:
    def __init__(self, matrix=None, n_size=9):
        self.matrix = matrix if matrix else self.generate_board(n_size)
        self.num_cols = n_size
        self.num_rows = n_size
    
    # i = row value for sudoku matrix [0-n)
    # j = column value for sudoku matrix [0-n)
    def validate_update(self, row, col, value):       
        # detect if value is in this row or column
        for i in range(len(self.matrix)):
            if value == self.matrix[i][col] or value == self.matrix[row][i]:
                return False

        # detect 3x3 region it is contained in
        region_row = 3*(row // 3) # 3 horizontal and vertical regions find region index (// 3),
        region_col = 3*(col // 3) # then convert to matrix index for top left cell (3 * region index)
        for i in range(3):
            for j in range(3):
                if value == self.matrix[region_row+i][region_col+j]:
                    return False

        return True

    def find_empty_cell(self):
        # manually iterate through all cells to find empty one
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == 0:
                    return i, j
        return None, None

    # solve board with a brute force method (backtracking)
    def backtrack_solve(self):
        # find any empty cell as target to solve
        target_row, target_col = self.find_empty_cell()
        # base case, all cells filled
        if target_row is None:
            return True # puzzle solved already
        
        # recursive case, empty cells exist
        for target_val in range(1, 10):
            if self.validate_update(target_row, target_col, target_val):
                self.matrix[target_row][target_col] = target_val
                if self.backtrack_solve():
                    return True# puzzle now solved
                
                # if no more valid updates exist,
                # erase this cell and try again with next target_val
                self.matrix[target_row][target_col] = 0
        
        # unsolvable branch
        return False
        
    def solution_count(self):
        num_solves = 0
        
        # find any empty cell as target to solve
        target_row, target_col = self.find_empty_cell()

        # if all cells filled, solution found
        if target_row is None:
            return 1 # puzzle solved already
        
        # recursive case, empty cells exist
        for target_val in range(1, 10):
            if self.validate_update(target_row, target_col, target_val):
                self.matrix[target_row][target_col] = target_val
                
                # aggregate solutions found
                num_solves += self.solution_count()
                
                # erase this cell and try again with next target_val
                self.matrix[target_row][target_col] = 0
        
        # return number of solutions found
        return num_solves
        
    # TODO: Create function to generate a **uniquely** solvable sudoku board
    def generate_board(self):
        self.matrix = [[0 for _ in range(9)]\
                            for _ in range(9)] # create 9x9 matrix
        return
        
    def print_board(self):
        for row in range(len(self.matrix)):
            print(self.matrix[row])
        print('\n')

# random sudoku board someone was struggling with on reddit
# https://www.reddit.com/r/sudoku/comments/1gc2oij/have_not_been_stuck_this_bad_in_a_long_time_what/
matrix = [[0,0,3, 0,4,0, 8,6,9],
          [0,8,4, 1,6,9, 0,0,0],
          [2,6,9, 0,0,0, 0,1,0],

          [0,0,5, 0,9,0, 7,0,6],
          [8,9,7, 6,0,4, 1,5,0],
          [0,0,0, 0,7,0, 0,9,0],

          [0,0,0, 0,5,0, 0,4,0],
          [0,0,2, 0,0,3, 6,7,5],
          [0,0,0, 4,0,6, 9,0,0]]

# "Deadly Pattern" - 2 solutions
# https://www.reddit.com/r/sudoku/comments/1c35yrk/sudoku_with_2_solutions/
multi_solution_matrix = [[0,0,9, 4,1,5, 8,7,3],
                         [5,8,1, 7,6,3, 9,2,4],
                         [0,0,3, 9,2,8, 1,6,5],

                         [0,0,4, 1,5,7, 2,3,8],
                         [8,1,2, 3,9,6, 5,4,7],
                         [3,5,7, 2,8,4, 6,9,1],

                         [1,3,5, 6,7,2, 4,8,9],
                         [0,0,6, 8,3,1, 7,5,2],
                         [0,0,8, 5,4,9, 3,1,6]]

sudoku = Sudoku(matrix)
print("Board 1: ")
sudoku.print_board()
sudoku.backtrack_solve()
print("Board 1 (Solved): ")
sudoku.print_board()

malformed = Sudoku(multi_solution_matrix)
print("Board 2 (Malformed, 2 solutions): ")
malformed.print_board()
print(f'Number of calculated solutions: {malformed.solution_count()}') # prints 2, correct
