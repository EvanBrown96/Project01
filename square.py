# @file square.py
#  Source file for the square object
#
#  Project: Minesweeper
#  Author: Kristi Daigh
#  Created: 09/07/18


import tkinter as Tk



class Square(Tk.Label):

    """
    Square class for managing properties of a square in Minesweeper

    Attributes:
        is_mine: Boolean to record whether or not a square is a mine

        is_flagged: Boolean to record whether or not a square is flagged

        is_revealed: Boolean to record whether or not a square is revealed

        num_adj_mines: Integer to record number of mines adjacent to square

        was_moved: Boolean to record whether or not a square has been moved

        flag_img: Tk photoimage object of the flag

        mine_img: Tk photoimage object of the mine

        color_mapping: mapping of colors for each number of mines

    """

    # Constructor
    #  @author: Kristi
    def __init__(self, master, x, y, click_callback, rclick_callback, **options):
        """
        Constructor for Square class
        Initialized all attributes to false or 0 depending on type of Boolean
        or Integer

        Args:

            master: master window of this square widget

            x: column index of this square

            y: row index of this square

            click_callback: function to call when this square is clicked

            rclick_callback: function to call when this square is right-clicked

            options: keyword arguments to pass into the base Label widget

        """
        Tk.Label.__init__(self, master, options)

        # draw the square with proper stuff
        self.configure(bg="lightgray", relief=Tk.RAISED, font=("Futura", 24))

        # bind click and right click events
        self.bind("<Button-1>", lambda _: click_callback(x, y))
        self.bind("<Button-2>", lambda _: rclick_callback(x, y))
        self.bind("<Control-Button-1>", lambda _: rclick_callback(x, y))

        # images and colors to be used in the square
        self.flag_img = Tk.PhotoImage(file="./flag.gif")
        self.mine_img = Tk.PhotoImage(file="./mine.gif")
        self.color_mapping = {0: "black", 1: "blue3", 2: "green3", 3: "yellow", 4: "orange3", 5: "red3", 6: "maroon3", 7: "purple3", 8: "black"}

        # properties
        self.is_mine = False
        self.is_flagged = False
        self.is_revealed = False
        self.num_adj_mines = 0
        self.was_moved = False



    def flag(self):
        """
        flags the cell - sets property and displays image in cell
        """
        self.is_flagged = True
        self.configure(text="", image=self.flag_img)



    def unflag(self):
        """
        unflags the cell - sets property and hides image from cell
        """
        self.is_flagged = False
        self.configure(text="", image="")



    def reveal(self):
        """
        reveals the cell - sets property, number of mines in cell, mine image
        (if this cell is a mine), and relief to sunken
        """
        self.is_revealed = True
        self.configure(text=("" if self.is_mine or self.num_adj_mines == 0 else self.num_adj_mines),
                       image=(self.mine_img if self.is_mine else ""),
                       relief=Tk.SUNKEN, fg=self.color_mapping[self.num_adj_mines])



    def freeze(self):
        """
        removes bindings for mouse buttons - used for cheat mode and when game ends,
        to prevent user from editing cell
        """
        self.unbind("<Button-1>")
        self.unbind("<Button-2>")
        self.unbind("<Control-Button-1>")
