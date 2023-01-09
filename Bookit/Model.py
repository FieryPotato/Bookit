from pathlib import Path
import subprocess

from Bookit import Database, Move


USR: Path = Path('/Users/adrian.mac')
BOOKS: Path = USR / 'Books'
KOBO: Path = Path('/Volumes/KoboeReader')
DOWNLOADS: Path = USR / 'Downloads'
DB_PATH: Path = BOOKS / 'books.db'


class Model:
    def kobo_is_connected(self) -> bool:
        """Return whether kobo device is connected."""
        return KOBO.exists()

    def get_kobo_books(self) -> list[Move.Book]:
        """Return a list containing books currently on the Kobo."""
        books = [
            Move.Book(book.title, book.year, book.lname, book.fname, book.is_local)
            for book in Database.get_kobo_books()
        ]
        edited = [(book.title, book.lname, book.year) for book in books]
        return edited

    def get_local_books(self) -> list[Move.Book]:
        return [
            Move.Book(book.title, book.year, book.lname, book.fname, book.is_local)
            for book in Database.get_local_books()
        ]

    def move_local_to_kobo(self, title) -> None:
        book = Database.get_book(title)
        mover = Move.Mover(book=book)
        if mover.local_to_kobo():
            Database.update_book(book.title, book.year, book.lname, book.fname, True)

    def move_kobo_to_local(self, title) -> None:
        book = Database.get_book(title)
        mover = Move.Mover(book=book)
        if mover.kobo_to_local():
            Database.update_book(book.title, book.year, book.lname, book.fname, False)

    def add_book(self, path, title, year, lname, fname, is_local) -> None:
        book = Move.Book(title, year, lname, fname, is_local)
        mover = Move.Mover(source=Path(path), book=book)
        mover.install()
        Database.add_book(title, year, lname, fname, is_local)

    def remove_book(self, title) -> None:
        book = Database.get_book(title)
        mover = Move.Mover(book=book)
        mover.uninstall()
        Database.remove_book(title)

    def disconnect(self) -> None:
        subprocess.Popen(['diskutil', 'eject', KOBO])
