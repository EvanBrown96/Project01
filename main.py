## @file main.py
#  Main file for project
#
#  Project: Minesweeper
#  Author: All
#  Created: 09/06/18

from menu import Menu
import tkinter as Tk

root = Tk.Tk()

playing = Menu(root)
#playing.game_rules()
#playing.game_menu()
Tk.mainloop()
