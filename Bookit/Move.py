import shutil
from collections import namedtuple
from pathlib import Path



USR: Path = Path('/Users/adrian.mac')
BOOKS: Path = USR / 'Books'
KOBO: Path = Path('/Volumes/KoboeReader')
DB_PATH: Path = BOOKS / 'books.db'

Book = namedtuple('Book', ['title', 'year', 'lname', 'fname', 'is_local'])


class Mover:
    def __init__(self, source: Path = Path(), book: Book = None) -> None:
        if not source and not book:
            raise ValueError('Mover must be initialized with at least one '
                             'non-default argument.')
        self.source = source
        if book:
            self.book = book
            self.title = book.title
            self.year = book.year
            self.lname = book.lname
            self.fname = book.fname
            self.is_local = book.is_local
            if self.is_local:
                self.source = BOOKS / self.book_filename(source)
            else:
                self.source = KOBO / self.book_filename(source)
        if source:
            self.source = source
            if not self.book:
                self.book = self.get_book_from_path(source)

    @staticmethod
    def get_book_from_path(path: Path) -> Book:
        title, lname, year = path.stem.split('-')
        return Book(title, year, lname, '', None)

    def book_filename(self, source=None) -> str:
        """
        Returns the filename to be used for this book. Takes either a
        source parameter (path to the ebook file) or uses self.source.
        """
        if not source:
            source = self.source
        path_title = self.title.replace(' ', '-')
        path_lname = self.lname.replace(' ', '-')
        path_year = str(self.year)
        return f'{path_title}_{path_lname}_{path_year}{self.source.suffix}'

    def rename(self) -> None:
        """Rename self.source."""
        new_file_name = self.book_filename()

        # Rename self.source to new_file_name
        dst: Path = self.source.parent / new_file_name
        shutil.move(self.source, dst)

        # Change the file that self.source points to
        self.source = dst

    @property
    def local_path(self) -> Path:
        return BOOKS / self.book_filename()

    @property
    def kobo_path(self) -> Path:
        return KOBO / self.book_filename()

    def local_to_kobo(self) -> bool:
        """Move self.source to the device. Return whether move was successful."""
        if not self.local_path.exists():
            print('Book {self.book!r} does not exist.')
            return False
        shutil.move(self.local_path, self.kobo_path)
        return True

    def kobo_to_local(self) -> bool:
        """Move self.source to the local folder. Return whether move was successful."""
        if not self.kobo_path.exists():
            print('Book {self.book!r} does not exist.')
            return False
        shutil.move(self.kobo_path, self.local_path)
        return True

    def install(self) -> None:
        """Rename and move self.book to either local folder or kobo."""
        self.rename()
        if self.is_local:
            dst = BOOKS
        else:
            dst = KOBO
        shutil.move(self.source, dst)

    def uninstall(self) -> None:
        self.source.unlink(missing_ok=True)
