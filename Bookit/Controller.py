from Bookit.Model import Model
from Bookit.View import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.main_frame = self.view.main_frame

        self.initialize_kobo_books()
        self.initialize_local_books()



    def initialize_kobo_books(self) -> None:
        kobo_books = self.model.get_kobo_books()
        if not self.model.kobo_is_connected():
            book_list = ['Kobo Is Not Connected']
            for book in kobo_books:
                book_list.append(f'<{book}>')
            self.main_frame.kobo_book_var.set(book_list)
            return
        self.main_frame.kobo_book_var.set(kobo_books)

    def initialize_local_books(self) -> None:
        local_books = self.model.get_local_books()
        self.main_frame.local_book_var.set(local_books)
