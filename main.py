## @file main.py
#  Main file for project
#
#  Project: Minesweeper
#  Author: All
#  Created: 09/06/18

from menu import Menu

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
        self.playing = Menu()

    def begin(self):
        """
        Begins game by calling for game rules and game menu to be displayed
        """
        self.playing.game_rules()
        self.playing.game_menu()

driver = Main()
driver.begin()
