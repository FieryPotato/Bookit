import shutil
from collections import namedtuple
from pathlib import Path



USR: Path = Path('/Users/adrian.mac')
BOOKS: Path = USR / 'Books'
KOBO: Path = Path('/Volumes/KoboeReader')
DB_PATH: Path = BOOKS / 'books.db'

Book = namedtuple('Book', ['title', 'year', 'lname', 'fname', 'is_local'])


class Mover:
    def __init__(self, source: Path = None, book: Book = None) -> None:
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
            if not source:
                if self.is_local:
                    self.source = BOOKS / self.book_filename()
                else:
                    self.source = KOBO / self.book_filename()
        if source:
            self.source = source
            if not self.book:
                self.book = self.get_book_from_path(source)

        self._kobo_path = None
        self._local_path = None

    def kobo_books(self) -> list[Path]:
        return list(KOBO.glob('[!.]*.[!.db]*'))

    def local_books(self) -> list[Path]:
        return list(BOOKS.glob('[!.]*.[!.db]*'))

    @staticmethod
    def get_book_from_path(path: Path) -> Book:
        title, lname, year = path.stem.split('-')
        return Book(title, year, lname, '', None)

    def book_filename(self, source=None) -> Path:
        """
        Returns the filename to be used for this book. Takes either a
        source parameter (path to the ebook file) or uses self.source.
        """
        path_title = self.title.replace(' ', '-')
        path_lname = self.lname.replace(' ', '-')
        path_year = str(self.year)
        stem = f'{path_title}_{path_lname}_{path_year}'
        if source:
            suffix = self.source.suffix
        else:
            books = self.kobo_books() + self.local_books()
            book = next(book for book in books if book.stem == stem)
            suffix = book.suffix
        return Path(f'{stem}{suffix}')

    def rename(self) -> None:
        """Rename self.source."""
        new_file_name = self.book_filename()

        # Rename self.source to new_file_name
        dst: Path = self.source.parent / new_file_name
        shutil.move(self.source, dst)

        # Change the file that self.source points to
        self.source = dst

    def local_path(self) -> Path:
        if self._local_path is None:
            self._local_path = BOOKS / self.book_filename()
        return self._local_path

    def kobo_path(self) -> Path:
        if self._kobo_path is None:
            self._kobo_path = KOBO / self.book_filename()
        return self._kobo_path

    def local_to_kobo(self) -> None:
        """Move self.source to the device. Return whether move was successful."""
        if not self.local_path().exists():
            print(f'Book {self.book!r} does not exist.')
            return
        shutil.move(self.local_path(), self.kobo_path())

    def kobo_to_local(self) -> None:
        """Move self.source to the local folder. Return whether move was successful."""
        if not self.kobo_path().exists():
            print(f'Book {self.book!r} does not exist.')
            return
        shutil.move(self.kobo_path(), self.local_path())

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
