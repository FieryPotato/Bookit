import tkinter as tk
from tkinter import filedialog as fd

from Bookit.Model import Model, DOWNLOADS
from Bookit.View import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.main_frame = self.view.main_frame
        self.add_frame = self.view.add_book_frame
        self.refresh()

        # Configure Main Frame
        # Configure kobo book list.
        self.main_frame.kobo_books.bind('<<ListboxSelect>>', self.kobo_books_list_select)
        self.main_frame.kobo_books.bind('<Button-1>', self.kobo_books_list_select)

        # Configure Kobo <-- Local button.
        self.main_frame.to_kobo_button.configure(command=self.move_local_to_kobo)

        # Configure Kobo --> Local button.
        self.main_frame.to_local_button.configure(command=self.move_kobo_to_local)

        # Configure local book list.
        self.main_frame.local_books.bind('<<ListboxSelect>>', self.local_books_list_select)
        self.main_frame.local_books.bind('<Button-1>', self.local_books_list_select)

        # Configure Add Book Button.
        self.main_frame.add_book_button.configure(command=self.add_book_callback)

        # Configure Remove Book Button.
        self.main_frame.remove_book_button.configure(command=self.remove_book_callback)

        # Configure Disconnect Button.
        self.main_frame.disconnect_button.configure(command=self.disconnect_callback)

        # Configure Refresh Button.
        self.main_frame.refresh_button.configure(command=self.refresh)

        # Configure Quit button.
        self.main_frame.quit_button.configure(command=self.quit)

        # Configure Add Book Frame
        # Configure RadioButtons
        # Configure Continue Button
        self.add_frame.continue_button.configure(command=self.add_book_continue)
        # Configure Cancel Button
        self.add_frame.cancel_button.configure(command=self.surface_main_frame)

    def start(self) -> tk.Tk:
        self.view.title('Bookit')
        return self.view

    def initialize_kobo_books(self) -> None:
        kobo_books = self.model.get_kobo_books()
        if not self.model.kobo_is_connected():
            book_list = ['Kobo Is Not Connected']
            for book in kobo_books:
                book_list.append(f'{book}')
            self.main_frame.kobo_book_var.set(book_list)
            self.main_frame.kobo_books.configure(state=tk.DISABLED)
            return
        self.main_frame.kobo_book_var.set(kobo_books)

    def initialize_local_books(self) -> None:
        local_books = self.model.get_local_books()
        self.main_frame.local_book_var.set(local_books)

    def kobo_books_list_select(self, *_) -> None:
        if not self.model.kobo_is_connected():
            self.main_frame.to_kobo_button.configure(state=tk.DISABLED)
            self.main_frame.to_local_button.configure(state=tk.DISABLED)
        self.main_frame.remove_book_button.configure(state=tk.NORMAL)
        self.main_frame.to_kobo_button.configure(state=tk.DISABLED)
        self.main_frame.to_local_button.configure(state=tk.NORMAL)

    def local_books_list_select(self, *_) -> None:
        if not self.model.kobo_is_connected():
            self.main_frame.to_kobo_button.configure(state=tk.DISABLED)
            self.main_frame.to_local_button.configure(state=tk.DISABLED)
        self.main_frame.remove_book_button.configure(state=tk.NORMAL)
        self.main_frame.to_kobo_button.configure(state=tk.NORMAL)
        self.main_frame.to_local_button.configure(state=tk.DISABLED)

    def move_local_to_kobo(self) -> None:
        selection = self.main_frame.local_books.selection_get()
        self.model.move_local_to_kobo(selection)
        self.refresh()

    def move_kobo_to_local(self) -> None:
        selection = self.main_frame.kobo_books.selection_get()
        self.model.move_kobo_to_local(selection)
        self.refresh()

    def add_book_callback(self) -> None:
        """Callback for the Add Book button in the Main frame."""
        self.surface_add_book()
        self.refresh()

    def add_book_continue(self) -> None:
        """Callback for the Continue button in the Add Book frame."""
        path: str = fd.askopenfilename(initialdir=DOWNLOADS)
        title = self.add_frame.title_entry_var.get()
        fname = self.add_frame.fname_entry_var.get()
        lname = self.add_frame.lname_entry_var.get()
        year = int(self.add_frame.year_entry_var.get())
        is_local = self.add_frame.radio_var.get()
        self.model.add_book(
            path=path,
            title=title,
            year=year,
            lname=lname,
            fname=fname,
            is_local=is_local
        )
        self.refresh()
        self.surface_main_frame()

    def remove_book_callback(self) -> None:
        if self.main_frame.kobo_books.curselection():
            book = self.main_frame.kobo_books.selection_get()
        elif self.main_frame.local_books.curselection():
            book = self.main_frame.local_books.selection_get()
        else:
            return
        self.model.remove_book(book)
        self.refresh()

    def disconnect_callback(self) -> None:
        self.model.disconnect()
        self.initialize_kobo_books()
        self.refresh()

    def surface_add_book(self):
        self.pack_forget()
        self.view.add_book_frame.pack()
        self.reset_fields()

    def surface_main_frame(self):
        self.pack_forget()
        self.view.main_frame.pack()
        self.reset_fields()

    def reset_fields(self) -> None:
        for frame in self.view.frames:
            for attribute, variable in frame.defaults.items():
                getattr(frame, attribute).set(variable)

    def pack_forget(self) -> None:
        for frame in self.view.frames:
            frame.pack_forget()

    def refresh(self) -> None:
        if self.model.kobo_is_connected():
            self.main_frame.disconnect_button.configure(state=tk.NORMAL)
            self.add_frame.radio_var.set(False)
            self.add_frame.kobo_radio.configure(state=tk.NORMAL)
        else:
            self.main_frame.disconnect_button.configure(state=tk.DISABLED)
            self.add_frame.radio_var.set(True)
            self.add_frame.kobo_radio.configure(state=tk.DISABLED)
        self.initialize_local_books()
        self.initialize_kobo_books()
        max_width = max(len(str(item)) for item in self.main_frame.listbox_contents)
        for listbox in self.main_frame.listboxes:
            listbox.configure(width=max_width)

    def quit(self) -> None:
        self.view.destroy()
