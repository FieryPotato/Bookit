import tkinter as tk


class View(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.main_frame = MainFrame(self)
        self.frames = self.main_frame,


class MainFrame(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)

        self.list_var_height = 16

        # KoboBooksList
        self.kobo_book_var = tk.Variable()
        self.kobo_books = tk.Listbox(self,
                                     listvariable=self.kobo_book_var,
                                     height=self.list_var_height)
        self.kobo_books.pack(side=tk.LEFT)

        # XferButtonContainer
        self.xfer_buttons = tk.Frame(self)
        self.xfer_buttons.pack(side=tk.LEFT)

        # ToKoboButton
        self.to_kobo_button = tk.Button(self.xfer_buttons, text='\u27F5')
        self.to_kobo_button.pack(side=tk.TOP)

        # ToLocalButton
        self.to_local_button = tk.Button(self.xfer_buttons, text='\u27F6')
        self.to_local_button.pack(side=tk.BOTTOM)

        # LocalBooksContainer
        self.local_book_var = tk.Variable()
        self.local_books = tk.Listbox(self,
                                      listvariable=self.local_book_var,
                                      height=self.list_var_height)
        self.local_books.pack(side=tk.LEFT)

        # UtilityButtonContainer
        self.utility_buttons = tk.Frame(self)
        self.utility_buttons.pack()

        # AddBookButton
        self.add_book_button = tk.Button(self.utility_buttons,
                                         text='Add Book')
        self.add_book_button.pack(side=tk.BOTTOM)

        # RemoveBookButton
        self.remove_book_button = tk.Button(self.utility_buttons,
                                            text='Remove Book')
        self.remove_book_button.pack(side=tk.BOTTOM)

        # QuitButton
        self.quit_button = tk.Button(self.utility_buttons,
                                     text='Quit')
        self.quit_button.pack(side=tk.BOTTOM)
