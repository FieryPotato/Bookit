from pathlib import Path

import sqlalchemy.orm

USR: Path = Path('/Users/adrian.mac')
BOOKS: Path = USR / 'Books'
KOBO: Path = Path('/Volumes/KoboeReader')
DOWNLOADS: Path = USR / 'Downloads'
DB_PATH: Path = BOOKS / 'books.db'

Base = sqlalchemy.orm.declarative_base()
ENGINE_PATH = 'sqlite:///' + str(DB_PATH)


class Book(Base):
    __tablename__ = 'book'

    title = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    year = sqlalchemy.Column(sqlalchemy.Integer)
    lname = sqlalchemy.Column(sqlalchemy.String)
    fname = sqlalchemy.Column(sqlalchemy.String)
    is_local = sqlalchemy.Column(sqlalchemy.Boolean)

    def __repr__(self):
        return f'Book(title={self.title!r}, year={self.year!r}, ' \
               f'lname={self.lname!r}, fname={self.fname!r}, ' \
               f'local={self.is_local!r}'


def sql_engine():
    return sqlalchemy.create_engine(ENGINE_PATH, future=True)


def add_book(title: str, year: int, lname: str, fname: str, is_local: bool) -> None:
    with sqlalchemy.orm.Session(sql_engine()) as session:
        new_book = Book(title=title, year=year, lname=lname, fname=fname, is_local=is_local)
        session.add(new_book)
        session.commit()


def update_book(title: str, year: int, lname: str, fname: str, is_local: bool) -> None:
    with sqlalchemy.orm.Session(sql_engine()) as session:
        statement = sqlalchemy.select(Book).where(Book.title == title)
        book = session.scalar(statement)

        book.title = title
        book.year = year
        book.lname = lname
        book.fname = fname
        book.is_local = is_local

        session.commit()


def get_book(title: str) -> Book:
    with sqlalchemy.orm.Session(sql_engine()) as session:
        statement = sqlalchemy.select(Book).where(Book.title == title)
        book = session.scalar(statement)
    if book is None:
        raise ValueError(f'Requested title \'{title}\' not in database.')
    return book


def remove_book(title: str) -> None:
    with sqlalchemy.orm.Session(sql_engine()) as session:
        session.execute(sqlalchemy.delete(Book).where(Book.title == title))
        session.commit()


def get_column(column: str) -> list[str]:
    if column not in {'title', 'year', 'lname', 'fname', 'is_local'}:
        raise ValueError(f'Requested column \'{column}\' not in database.')
    with sqlalchemy.orm.Session(sql_engine()) as session:
        statement = sqlalchemy.select(getattr(Book, column))
        column_scalar = session.scalars(statement)
        if not column_scalar:
            column_contents = ['Database includes no books.']
        else:
            column_contents = column_scalar.fetchall()
    return column_contents


if not DB_PATH.exists():
    if not BOOKS.exists():
        BOOKS.mkdir()
    Base.metadata.create_all(sql_engine())


def get_kobo_books() -> list[Book]:
    with sqlalchemy.orm.Session(sql_engine()) as session:
        statement = sqlalchemy.select(Book).where(Book.is_local == False)
        scalars = session.scalars(statement)
        if not scalars:
            return []
        return scalars.fetchall()


def get_local_books():
    with sqlalchemy.orm.Session(sql_engine()) as session:
        statement = sqlalchemy.select(Book).where(Book.is_local == True)
        scalars = session.scalars(statement)
        if not scalars:
            return []
        return scalars.fetchall()
