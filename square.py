## @file square.py
#  Source file for the square object
#
#  Project: Minesweeper
#  Author: Kristi Daigh
#  Created: 09/07/18


## @class Square
#  @brief Defines and manages properties for Square object
class Square:

    ## Constructor
    #  @author: Kristi
    def __init__(self):
        ## @var is_mine
        #  mine status flag
        self.is_mine = False
        ## @var is_flagged
        #  flag status flag
        self.is_flagged = False
        ## @var is_revealed
        #  reveal status flag
        self.is_revealed = False
        ## @var num_adj_mines
        #  tracks number of adjacent mines
        self.num_adj_mines = 0
        ## @var was_moved
        # tracks what mines were moved
        self.was_moved = False
        
    ## Prints the square based on properties
    #  @author: Kristi
    def print_square(self):
        if not self.is_revealed:
            if self.is_flagged:
                print(str("F").ljust(2), end=' ')
            else:
                print(str("#").ljust(2), end=' ')
        else:
            if self.is_mine:
                print(str("*").ljust(2), end=' ')
            elif self.num_adj_mines:
                print(str(self.num_adj_mines).ljust(2), end=' ')
            else:
                print(str(" ").ljust(2), end=' ')
