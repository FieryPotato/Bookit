import tkinter as tk

from Bookit.Model import Model
from Bookit.View import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.main_frame = self.view.main_frame

        # Initialize book lists.
        self.initialize_kobo_books()
        self.initialize_local_books()

        # Configure kobo book list.
        self.main_frame.kobo_books.bind('<<ListboxSelect>>', self.kobo_books_list_select)

        # Configure local book list.
        self.main_frame.local_books.bind('<<ListboxSelect>>', self.local_books_list_select)

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
        if not self.main_frame.kobo_book_var.get():
            return
        self.main_frame.to_kobo_button.configure(state=tk.DISABLED)
        self.main_frame.to_local_button.config(state=tk.NORMAL)

    def local_books_list_select(self, *_) -> None:
        if not self.model.kobo_is_connected():
            return
        if not self.main_frame.local_book_var.get():
            return
        self.main_frame.to_kobo_button.configure(state=tk.NORMAL)
        self.main_frame.to_local_button.config(state=tk.DISABLED)

    def quit(self) -> None:
        self.view.destroy()
