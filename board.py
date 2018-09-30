## @file board.py
#  Source file for the board object
#
#  Project: Minesweeper
#  Author: Clare Meyer
#  Created: 09/06/18

from random import randint
from square import Square


## @class Board
#  @brief Handles board creation and board functionality
class Board:

    ## Constructor
    #  @author: Clare
    def __init__(self):
        ## @var boardSize
        #  stores the size of the board
        self.boardWidth = 0
        self.boardHeight = 0
        ## @var mines_num
        #  stores the number of mines
        self.mines_num = 0

    ## Generates a grid object
    #  @author: Clare
    #  @param: size, size of the grid
    #  @returns: grid
    def make_grid(self, width, height):
        width = int(width)
        height = int(height)
        grid = [[0 for y in range(height)] for x in range(width)]
        for i in range(0, width):
            for j in range(0, height):
                grid[i][j] = Square()
        return grid

    ## Randomly places mines on board
    #  @author: Ayah
    #  @pre: a grid has been generated
    #  @param: num_mines, user-selected number of mines
    #  @param: size, size of the grid
    #  @param: grid, grid to be populated
    #  @post: the grid is populated with mines
    def generate_mines(self, mines, width, height, grid):
        self.mines_num=mines;
        self.boardWidth = width;
        self.boardHeight = height;
        for i in range(0, self.mines_num):
            is_bomb = False
            while not is_bomb:
                a = randint(0, self.boardWidth - 1)
                b = randint(0, self.boardHeight - 1)
                if not grid[a][b].is_mine:
                    grid[a][b].is_mine = True
                    is_bomb = True

    ## Prints the board with minimal formatting
    #  @author:Clare
    #  @pre: the grid has been generated
    #  @param: size, size of the grid
    #  @param: grid, grid to be printed
    #  @post: grid printed in a grid-like manner
    def just_print(self, size, grid):
        for i in range(0, size):
            for j in range(0, size):
                grid[i][j].print_square()
            print('\n', end=' ')

    ## Prints a formatted game board
    #  @author: Clare
    #  @pre: grid does not have formatting
    #  @param: size, size of the grid
    #  @param: main_grid, grid to be printed
    #  @post: grid is printed to look nice for the user
    def print_board(self, width, height, main_grid):
            width = int(width)
            height = int(height)

            grid = [[0 for x in range(height + 2)] for y in range(width + 2)]

            for i in range(0, height+2):
                for j in range(0, width+2):
                    if(i == 0 and j == 0 or i == 0 and j == 1 or i == 1 and j == 0
                    or i == 1 and j == 1):
                        grid[j][i] = " "
                    elif j == 0:
                        grid[j][i] = i-2
                    elif i == 0:
                        grid[j][i] = j-2
                    elif j == 1:
                        grid[j][i] = "|"
                    elif i == 1:
                        grid[j][i] = "--"
                    else:
                        grid[j][i] = main_grid[j - 2][i - 2]

            for i in range(0, height+2):
                for j in range(0, width+2):
                    if i == 0 or i == 1 or j == 0 or j == 1:
                        if i == 1 and j == 0:
                            print(grid[j][i], end=' ')
                        elif i == 0 and j == 0 or i == 0 and j == 1 or i == 1 and j == 1:
                            print((str(grid[j][i]).ljust(2)), end=' ')
                        elif i == 0 or j == 0:
                            print((str(grid[j][i]).zfill(2)), end=' ')
                        else:
                            print(str(grid[j][i]).ljust(2), end=' ')
                    else:
                        grid[j][i].print_square()
                print('\n', end=' ')

    ## Counts number of adjacent mines for a given cell
    #  @authors: Kyle, Kristi
    #  @param x, x-coordinate of cell
    #  @param y, y-coordinate of cell
    #  @param: size, size of the grid
    #  @param: grid, grid to be checked
    def count_nearby_mines(self, x, y, width, height, grid):
        if grid[x][y].is_mine:
            return

        for i in range(-1, 2):
            if x+i >= 0 and x+i < width:
                for j in range(-1, 2):
                    if y+j >= 0 and y+j < height:
                        if grid[x+i][y+j].is_mine:
                            grid[x][y].num_adj_mines += 1

    #Simple loop to reset num_adj_mines to 0 before being evaluated again
    def resetGridMineCount(self, grid):
        for x in range(0, self.boardWidth):
            for y in range(0, self.boardHeight):
                grid[x][y].num_adj_mines = 0;


    ## Counts/labels number of adjacent mines for board
    #  @author: Kyle
    #  @param: size, size of the grid
    #  @param: grid, grid to be checked
    #  @post: each square is labeled with num_adj_mines
    def mine_check(self, width, height, grid):
        for x in range(width):
            for y in range(height):
                #grid[x][y].num_adj_mines = 0;
                oldCount = grid[x][y].num_adj_mines
                self.count_nearby_mines(x, y, width, height, grid)
