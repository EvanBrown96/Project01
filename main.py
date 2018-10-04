# @file main.py
#  Main file for project
#
#  Project: Minesweeper
#  Author: All
#  Created: 09/06/18

from menu import Menu
import tkinter as Tk


class Main:
    """
    Source file for project. Creates instance of Menu class, begins game by
    the rules and menu

    Attributes:
        playing: Instance of the Menu class
    """

    def __init__(self):
        """
        Constructor for Main class

        Initializes all attributes
        """
        root = Tk.Tk()
        self.playing = Menu(root)


Main()
Tk.mainloop()
