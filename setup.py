import tkinter as Tk
from tkinter import messagebox
from executive import Executive
from window_functions import center_window

class Setup:

    def __init__(self, root, menu_callback):

        self.exec = Executive()
        self.root = root
        self.bg = "indianred2"
        self.menu_callback = menu_callback

        self.setup_window = Tk.Toplevel(root)
        self.setup_window.geometry("200x200")
        center_window(self.setup_window)

        self.setup_window.withdraw()
        self.setup_window.deiconify()

        self.setup_window.title("Setup Board")
        self.setup_window.configure(bg=self.bg, bd=10, relief="ridge", pady=32)
        self.setup_window.resizable(width=False, height=False)

        def return_to_menu():
            self.setup_window.destroy()
            self.menu_callback()

        self.setup_window.protocol("WM_DELETE_WINDOW", return_to_menu)
        self.setup_window.bind("<Escape>", lambda _: return_to_menu())
        self.setup_window.bind("<Return>", lambda _: self.validate())

        self.width_val = Tk.StringVar()
        self.height_val = Tk.StringVar()
        self.mines_val = Tk.StringVar()

        self.width_text = Tk.Label(self.setup_window, text="Width", bg=self.bg)
        self.width_input = Tk.Entry(self.setup_window, width=12, highlightbackground=self.bg, textvariable=self.width_val)

        self.width_text.grid(row=0, column=0, sticky=Tk.E)
        self.width_input.grid(row=0, column=1)

        self.height_text = Tk.Label(self.setup_window, text="Height", bg=self.bg)
        self.height_input = Tk.Entry(self.setup_window, width=12, highlightbackground=self.bg, textvariable=self.height_val)

        self.height_text.grid(row=1, column=0, sticky=Tk.E)
        self.height_input.grid(row=1, column=1)

        self.mines_text = Tk.Label(self.setup_window, text="Mines", bg=self.bg)
        self.mines_input = Tk.Entry(self.setup_window, width=12, highlightbackground=self.bg, textvariable=self.mines_val)

        self.mines_text.grid(row=2, column=0, sticky=Tk.E)
        self.mines_input.grid(row=2, column=1)

        self.begin = Tk.Button(self.setup_window, text="Begin Game", command=self.validate, highlightbackground=self.bg)
        self.begin.grid(row=3, column=0, columnspan=2)


    def validate(self):

        def checknum(val):

            if len(val) == 0:
                return False

            for i in range(len(val)):
                if not val[i].isdigit():
                    return False

            return True

        width = self.width_input.get()
        height = self.height_input.get()
        mines = self.mines_input.get()

        if not checknum(width):
            messagebox.showerror("Entry Error", "Board width must be a number!")
        elif not checknum(height):
            messagebox.showerror("Entry Error", "Board height must be a number!")
        elif not checknum(mines):
            messagebox.showerror("Entry Error", "Mine count must be a number!")
        else:

            width = int(width)
            height = int(height)
            mines = int(mines)

            if width < 2:
                messagebox.showerror("Entry Error", "Too small of a width")
            elif width > 15:
                messagebox.showerror("Entry Error", "Too large of a width")
            elif height < 2:
                messagebox.showerror("Entry Error", "Too small of a height")
            elif height > 15:
                messagebox.showerror("Entry Error", "Too large of a height")
            elif mines >= width * height:
                messagebox.showerror("Entry Error", "Too many mines!")
            elif mines < 1:
                messagebox.showerror("Entry Error", "Too few mines!")
            else:
                self.setup_window.destroy()
                self.exec.setup(width, height, mines)
                self.exec.play()
                self.menu_callback()
