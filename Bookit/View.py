import tkinter as tk


class View(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.main_frame = MainFrame(self)
        self.frames = self.main_frame,


class MainFrame(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)

        # KoboBooksContainer
        kobo_books = tk.Frame(self)
        kobo_books.pack()

        # XferButtonContainer
        xfer_buttons = tk.Frame(self)

        # LocalBooksContainer
        local_books = tk.Frame(self)

        # UtilityButtonContainer
        utility_buttons = tk.Frame(self)

