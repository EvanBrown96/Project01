def center_window(window):
    """
    centers the given window/widget on the screen

    Args:

        window: the tk window (root/toplevel) instance to center

    """
    window.attributes('-alpha', 0.0)
    window.update_idletasks()
    # get current window width & height
    width = window.winfo_width()
    height = window.winfo_height()
    # calculate centered x and y
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    # resize window
    window.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
    window.attributes('-alpha', 1.0)