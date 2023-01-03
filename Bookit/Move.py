import shutil
from pathlib import Path


USR: Path = Path('/Users/adrian.mac')
BOOKS: Path = USR / 'Books'
KOBO: Path = Path('/Volumes/KoboeReader')
DB_PATH: Path = BOOKS / 'books.db'


class Mover:
    def __init__(self, source: Path) -> None:
        self.source: Path = source
        self.name = source.name

    def rename(self, title: str, lname: str, year: int) -> None:
        """Rename self.source."""
        # Create new file name based on book information.
        path_title = title.replace(' ', '-')
        path_lname = lname.replace(' ', '-')
        path_year = str(year)
        new_file_name = f'{path_title}_{path_lname}_{path_year}{self.source.suffix}'

        # Rename self.source to new_file_name
        dst: Path = self.source.parent / new_file_name
        shutil.move(self.source, dst)

        # Change the file that self.source points to
        self.source = dst
        self.name = new_file_name

    def move_to_kobo(self) -> None:
        """Move self.source to the device."""
        shutil.move(self.source, KOBO / self.name)

    def move_to_local(self) -> None:
        """Move self.source to the local folder."""
        shutil.move(self.source, BOOKS / self.name)
