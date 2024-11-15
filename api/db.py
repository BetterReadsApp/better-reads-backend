from api.model.quiz import Quiz
from api.model.rating import Rating
from api.settings import DATABASE_URL
from sqlmodel import create_engine, SQLModel, Session, select, or_
from fastapi import HTTPException
from datetime import date
from api.model.user import User
from api.model.book import Book
from api.model.shelf import Shelf
from api.model.enums.book_genre import BookGenre

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
    # create_books(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_user_by_field(field_name: str, value: str, session: Session):
    query = select(User).where(getattr(User, field_name) == value)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_users_by_name_and_last_name(name: str, last_name: str, session: Session):
    query = select(User)
    if name or last_name:
        query = query.where(
            or_(
                User.name.ilike(f"%{name}%") if name else False,
                User.last_name.ilike(f"%{last_name}%") if last_name else False,
            )
        )

    return session.exec(query).all()


def get_book_by_id(book_id: int, session: Session):
    query = select(Book).where(Book.id == book_id)
    book = session.exec(query).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def get_shelf_by_id(shelf_id: int, session: Session):
    query = select(Shelf).where(Shelf.id == shelf_id)
    shelf = session.exec(query).first()
    if not shelf:
        raise HTTPException(status_code=404, detail="Shelf not found")
    return shelf


def user_exists_by_field(field_name: str, value: str, session: Session) -> bool:
    query = select(User).where(getattr(User, field_name) == value)
    user = session.exec(query).first()

    return user is not None


def get_rated_books_by_user_id(user_id: int, session: Session):
    query = select(Book).join(Book.ratings).where(Rating.user_id == user_id)
    return session.exec(query).all()


def get_read_books_by_user_id(user_id: int, session: Session):
    query = select(Shelf).where(Shelf.name == "Read", Shelf.user_id == user_id)
    shelf = session.exec(query).first()
    if not shelf:
        return []
    return shelf.books


def get_books_by_authors(books: list[Book], session: Session):
    new_books = []
    for book in books:
        query = select(Book).where(Book.author == book.author)
        new_books.extend(session.exec(query).all())
    return new_books


def get_books_by_genre(books: list[Book], session: Session):
    new_books = []
    for book in books:
        query = select(Book).where(Book.genre == book.genre)
        new_books.extend(session.exec(query).all())
    return new_books


def get_quiz_by_id(quiz_id: int, session: Session):
    query = select(Quiz).where(Quiz.id == quiz_id)
    quiz = session.exec(query).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


def create_books(engine):
    with Session(engine) as session:
        carrie = Book(
            title="Carrie",
            summary="Carrie White, a shy, friendless teenage",
            author="Stephen King",
            pages=199,
            publication_date=date(1974, 4, 5),
            genre=BookGenre.HORROR,
        )
        it = Book(
            title="It",
            summary="Ohhh scary...",
            author="Stephen King",
            pages=1116,
            publication_date=date(1986, 9, 15),
            genre=BookGenre.HORROR,
        )
        the_shining = Book(
            title="The Shining",
            summary="A family heads to an isolated hotel for the winter where an evil presence influences the father into violence.",
            author="Stephen King",
            pages=447,
            publication_date=date(1977, 1, 28),
            genre=BookGenre.HORROR,
        )
        misery = Book(
            title="Misery",
            summary="A famous author is held captive by a deranged fan who demands he writes her preferred ending.",
            author="Stephen King",
            pages=338,
            publication_date=date(1987, 6, 8),
            genre=BookGenre.HORROR,
        )
        pet_semetary = Book(
            title="Pet Sematary",
            summary="A family discovers a burial ground with the power to bring back the dead, but at a terrible cost.",
            author="Stephen King",
            pages=374,
            publication_date=date(1983, 11, 14),
            genre=BookGenre.HORROR,
        )
        session.add_all([carrie, it, the_shining, misery, pet_semetary])
        session.commit()
