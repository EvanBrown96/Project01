# @file square.py
#  Source file for the square object
#
#  Project: Minesweeper
#  Author: Kristi Daigh
#  Created: 09/07/18


import tkinter as Tk

# @class Square
#  @brief Defines and manages properties for Square object
class Square(Tk.Label):

    """
    Square class for managing properties of a square in Minesweeper

    Attributes:
        is_mine: Boolean to record whether or not a square is a mine

        is_flagged: Boolean to record whether or not a square is flagged

        is_revealed: Boolean to record whether or not a square is revealed

        num_adj_mines: Integer to record number of mines adjacent to square

        was_moved: Boolean to record whether or not a square has been moved
    """

    # Constructor
    #  @author: Kristi
    def __init__(self, master, x, y, click_callback, rclick_callback, **options):
        """
        Constructor for Square class
        Initialized all attributes to false or 0 depending on type of Boolean
        or Integer
        """
        Tk.Label.__init__(self, master, options)
        self.configure(bg="lightgray", relief=Tk.RAISED)
        self.is_mine = False
        self.is_flagged = False
        self.is_revealed = False
        self.num_adj_mines = 0
        self.was_moved = False
        self.bind("<Button-1>", lambda _: click_callback(x, y))
        self.bind("<Button-2>", lambda _: rclick_callback(x, y))
        self.bind("<Control-Button-1>", lambda _: rclick_callback(x, y))
        self.flag_img = Tk.PhotoImage(file="./flag.gif")
        self.mine_img = Tk.PhotoImage(file="./mine.gif")

    def flag(self):
        self.is_flagged = True
        self.configure(text="", image=self.flag_img)
    def unflag(self):
        self.is_flagged = False
        self.configure(text="", image="")
    def reveal(self):
        self.is_revealed = True
        self.configure(text=("" if self.is_mine or self.num_adj_mines == 0 else self.num_adj_mines),
                       image=(self.mine_img if self.is_mine else ""),
                       relief=Tk.SUNKEN)

    def freeze(self):
        self.unbind("<Button-1>")
        self.unbind("<Button-2>")
        self.unbind("<Control-Button-1>")

    ## Prints the square based on properties
    #  @author: Kristi
    def print_square(self):
        """
        Prints the square with respect to the current status of the square's
        attributes
        """
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
