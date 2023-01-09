import tkinter as tk


class View(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.main_frame = MainFrame(self)
        self.add_book_frame = AddBookFrame(self)
        self.main_frame.pack()

        self.frames = self.main_frame, self.add_book_frame


class MainFrame(tk.Frame):
    defaults = {}

    list_var_height = 16
    list_var_width = 30

    def __init__(self, master=None) -> None:
        super().__init__(master)


        # KoboBooksList
        self.kobo_book_var = tk.Variable()
        self.kobo_books = tk.Listbox(self,
                                     listvariable=self.kobo_book_var,
                                     height=self.list_var_height,
                                     width=self.list_var_width)
        self.kobo_books.pack(side=tk.LEFT)
        self.kobo_scroll_bar = tk.Scroll

        # XferButtonContainer
        self.xfer_buttons = tk.Frame(self)
        self.xfer_buttons.pack(side=tk.LEFT)

        # ToKoboButton
        self.to_kobo_button = tk.Button(self.xfer_buttons,
                                        state=tk.DISABLED,
                                        text='\u27F5')
        self.to_kobo_button.pack(side=tk.TOP)

        # ToLocalButton
        self.to_local_button = tk.Button(self.xfer_buttons,
                                         state=tk.DISABLED,
                                         text='\u27F6')
        self.to_local_button.pack(side=tk.BOTTOM)

        # LocalBooksContainer
        self.local_book_var = tk.Variable()
        self.local_books = tk.Listbox(self,
                                      listvariable=self.local_book_var,
                                      height=self.list_var_height,
                                      width=self.list_var_width)
        self.local_books.pack(side=tk.LEFT)

        # UtilityButtonContainer
        self.utility_buttons = tk.Frame(self)
        self.utility_buttons.pack(side=tk.LEFT)

        # AddBookButton
        self.add_book_button = tk.Button(self.utility_buttons,
                                         text='Add Book')
        self.add_book_button.pack()

        # RemoveBookButton
        self.remove_book_button = tk.Button(self.utility_buttons,
                                            text='Remove Book',
                                            state=tk.DISABLED)
        self.remove_book_button.pack()

        # DisconnectButton
        self.disconnect_button = tk.Button(self.utility_buttons,
                                           text='Disconnect Kobo',
                                           state=tk.DISABLED)
        self.disconnect_button.pack()

        # RefreshButton
        self.refresh_button = tk.Button(self.utility_buttons,
                                        text='Refresh')
        self.refresh_button.pack()

        # QuitButton
        self.quit_button = tk.Button(self.utility_buttons,
                                     text='Quit')
        self.quit_button.pack(side=tk.BOTTOM)


class AddBookFrame(tk.Frame):
    title_default = "Title"
    author_fname_default = "Author First Name"
    author_lname_default = "Author Last Name"
    year_default = "Year"
    defaults = {
        'title_entry_var': title_default,
        'fname_entry_var': author_fname_default,
        'lname_entry_var': author_lname_default,
        'year_entry_var': year_default,
    }

    def __init__(self, master=None) -> None:
        super().__init__(master)

        # Title Entry
        self.title_entry_var = tk.StringVar(value=self.title_default)
        self.title_entry = tk.Entry(master=self, textvariable=self.title_entry_var)
        self.title_entry.pack()

        # Author First Name Entry
        self.fname_entry_var = tk.StringVar(value=self.author_fname_default)
        self.fname_entry = tk.Entry(master=self, textvariable=self.fname_entry_var)
        self.fname_entry.pack()

        # Author Last Name Entry
        self.lname_entry_var = tk.StringVar(value=self.author_lname_default)
        self.lname_entry = tk.Entry(master=self, textvariable=self.lname_entry_var)
        self.lname_entry.pack()

        # Year Entry
        self.year_entry_var = tk.StringVar(value=self.year_default)
        self.year_entry = tk.Entry(master=self, textvariable=self.year_entry_var)
        self.year_entry.pack()

        # Radio Buttons
        self.radio_container = tk.Frame(master=self)
        self.radio_container.pack()

        self.radio_var = tk.BooleanVar(value=False)
        self.kobo_radio = tk.Radiobutton(master=self.radio_container,
                                         text='Add to Kobo',
                                         value=False,
                                         variable=self.radio_var)
        self.kobo_radio.pack(side=tk.RIGHT)
        self.local_radio = tk.Radiobutton(master=self.radio_container,
                                          text='Save Locally',
                                          value=True,
                                          variable=self.radio_var)
        self.local_radio.pack(side=tk.RIGHT)

        # Button Container Frame
        self.button_container = tk.Frame(master=self)
        self.button_container.pack()

        self.continue_button = tk.Button(master=self.button_container,
                                         text='Continue')
        self.continue_button.pack(side=tk.RIGHT)

        # Cancel Button
        self.cancel_button = tk.Button(master=self.button_container,
                                       text='Cancel')
        self.cancel_button.pack(side=tk.LEFT)
