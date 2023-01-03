from collections import namedtuple
from pathlib import Path

from Bookit import Database

Book = namedtuple('Book', ['title', 'year', 'lname', 'fname', 'is_local'])

USR: Path = Path('/Users/adrian.mac')
BOOKS: Path = USR / 'Books'
KOBO: Path = Path('/Volumes/KoboeReader')
Downloads: Path = USR / 'Downloads'
DB_PATH: Path = BOOKS / 'books.db'


class Model:
    def kobo_is_connected(self) -> bool:
        """Return whether kobo device is connected."""
        return KOBO.exists()

    def get_kobo_books(self) -> list[Book]:
        """Return a list containing books currently on the Kobo."""
        return [
            Book(book.title, book.year, book.lname, book.fname, book.is_local)
            for book in Database.get_kobo_books()
        ]

    def get_local_books(self) -> list[Book]:
        return [
            Book(book.title, book.year, book.lname, book.fname, book.is_local)
            for book in Database.get_local_books()
        ]
