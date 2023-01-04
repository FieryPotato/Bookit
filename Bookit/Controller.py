import tkinter as tk

from Bookit.Model import Model
from Bookit.View import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.main_frame = self.view.main_frame
        self.refresh()

        # Configure kobo book list.
        self.main_frame.kobo_books.bind('<<ListboxSelect>>', self.kobo_books_list_select)

        # Configure Kobo <-- Local button.
        self.main_frame.to_kobo_button.configure(command=self.move_local_to_kobo)

        # Configure Kobo --> Local button.
        self.main_frame.to_local_button.configure(command=self.move_kobo_to_local)

        # Configure local book list.
        self.main_frame.local_books.bind('<<ListboxSelect>>', self.local_books_list_select)

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

    def start(self) -> tk.Tk:
        self.view.title('Bookit')
        return self.view

    def initialize_kobo_books(self) -> None:
        kobo_books = self.model.get_kobo_books()
        if not self.model.kobo_is_connected():
            book_list = ['Kobo Is Not Connected']
            for book in kobo_books:
                book_list.append(f'<{book}>')
            self.main_frame.kobo_book_var.set(book_list)
            self.main_frame.kobo_books.configure(state=tk.DISABLED)
            return
        self.main_frame.kobo_book_var.set(kobo_books)

    def initialize_local_books(self) -> None:
        local_books = self.model.get_local_books()
        self.main_frame.local_book_var.set(local_books)

    def kobo_books_list_select(self, *_) -> None:
        if not self.model.kobo_is_connected():
            return
        if not self.main_frame.kobo_books.selection_get():
            return
        self.main_frame.to_kobo_button.configure(state=tk.DISABLED)
        self.main_frame.to_local_button.configure(state=tk.NORMAL)
        self.main_frame.remove_book_button.configure(state=tk.NORMAL)

    def local_books_list_select(self, *_) -> None:
        if not self.model.kobo_is_connected():
            return
        if not self.main_frame.local_books.selection_get():
            return
        self.main_frame.to_kobo_button.configure(state=tk.NORMAL)
        self.main_frame.to_local_button.configure(state=tk.DISABLED)
        self.main_frame.remove_book_button.configure(state=tk.NORMAL)

    def move_local_to_kobo(self) -> None:
        selection = self.main_frame.local_books.selection_get()
        self.model.move_local_to_kobo(selection)
        self.refresh()

    def move_kobo_to_local(self) -> None:
        selection = self.main_frame.kobo_books.selection_get()
        self.model.move_kobo_to_local(selection)
        self.refresh()

    def add_book_callback(self) -> None:
        self.model.add_book()
        self.refresh()

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
        self.refresh()

    def refresh(self) -> None:
        if self.model.kobo_is_connected():
            self.main_frame.disconnect_button.configure(state=tk.NORMAL)
        else:
            self.main_frame.disconnect_button.configure(state=tk.DISABLED)
        self.initialize_local_books()
        self.initialize_kobo_books()

    def quit(self) -> None:
        self.view.destroy()
