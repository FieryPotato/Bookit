from pathlib import Path

import sqlalchemy.orm


USR: Path = Path('/Users/adrian.mac')
BOOKS: Path = USR / 'Books'
KOBO: Path = Path('/Volumes/KoboeReader')
Downloads: Path = USR / 'Downloads'
DB_PATH: Path = BOOKS / 'books.db'

Base = sqlalchemy.orm.declarative_base()
ENGINE_PATH = 'sqlite:///' + str(DB_PATH)


class Book(Base):
    __tablename__ = 'book'

    title =    sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    year =     sqlalchemy.Column(sqlalchemy.Integer)
    lname =    sqlalchemy.Column(sqlalchemy.String)
    fname =    sqlalchemy.Column(sqlalchemy.String)
    is_local = sqlalchemy.Column(sqlalchemy.Boolean)
    
    def __repr__(self):
        return f'Book(title={self.title!r}, year={self.year!r}, '\
               f'lname={self.lname!r}, fname={self.fname!r}, '\
               f'local={self.is_local!r}'


def sql_engine():
    return sqlalchemy.create_engine(ENGINE_PATH, echo=True, future=True)


def add_book(title: str, year: int, lname: str, fname: str, local: bool) -> None:
    with sqlalchemy.orm.Session(sql_engine()) as session:
        new_book = Book(title=title, year=year, lname=lname, fname=fname)
        session.add(new_book)
        session.commit()


def update_book(title: str, year: str, lname: str, fname: str) -> None:
    with sqlalchemy.orm.Session(sql_engine()) as session:
        statement = sqlalchemy.select(Book).where(Book.title == title)
        book = session.scalar(statement)

        book.title = title
        book.year = year
        book.lname = lname
        book.fname = fname

        session.commit()


def get_book(title: str) -> Book | None:
    with sqlalchemy.orm.Session(sql_engine()) as session:
        statement = sqlalchemy.select(Book).where(Book.title == title)
        book = session.scalar(statement)
    return book


def remove_book(name: str) -> None:
    with sqlalchemy.orm.Session(sql_engine()) as session:
        session.execute(sqlalchemy.delete(Book).where(Book.title == title))
        session.commit()


def get_column(column: str) -> list[str]:
    if column not in {'title', 'year', 'lname', 'fname'}:
        raise ValueError(f'Requested column \'{column}\' not in database.')
    with sqlalchemy.orm.Session(sql_engine()) as session:
        statement = sqlalchemy.select(getattr(Book, column))
        column_scalar = session.scalars(statement)
        if not column_scalar:
            column_contents = ['Database includes no books.']
        else:
            column_contents = column_scalar.fetchall()
    return column_contents


def move_local_to_kobo(title: str) -> None:
    if 


if not DB_PATH.exists():
    if not BOOKS.exists():
        BOOKS.mkdir()
    Base.metadata.create_all(sql_engine())
    

