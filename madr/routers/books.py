from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Book, Novelist, User
from madr.schemas import BookPublic, BookSchema, BookUpdate, Message
from madr.security import get_current_user
from madr.utils import sanitize

router = APIRouter(prefix='/books', tags=['books'])

T_CurrentUser = Annotated[User, Depends(get_current_user)]
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookSchema, session: T_Session, user: T_CurrentUser):
    novelist = session.scalar(
        select(Novelist).where(Novelist.id == book.novelist_id)
    )

    if not novelist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Novelist ID not found',
        )

    new_book = Book(year=book.year, title=sanitize(book.title))
    new_book.novelist = novelist

    try:
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Book already exists in MADR',
        )

    return new_book


@router.delete('/{book_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_book(book_id: int, session: T_Session, user: T_CurrentUser):
    book = session.scalar(select(Book).where(Book.id == book_id))

    if not book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not found in MADR',
        )

    session.delete(book)
    session.commit()

    return {'message': 'Book deleted from MADR'}


@router.patch(
    '/{book_id}', status_code=HTTPStatus.OK, response_model=BookSchema
)
def update_book(
    book_id: int, book: BookUpdate, session: T_Session, user: T_CurrentUser
):
    book_db = session.scalar(select(Book).where(Book.id == book_id))

    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not found in MADR',
        )

    try:
        book_db.novelist_id = book.novelist_id
        book_db.title = sanitize(book.title)
        book_db.year = book.year

        session.add(book_db)
        session.commit()
        session.refresh(book_db)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Book already exists in MADR',
        )

    return book_db


@router.get('/{book_id}', status_code=HTTPStatus.OK, response_model=BookPublic)
def read_book(book_id: int, session: T_Session, user: T_CurrentUser):
    book = session.scalar(select(Book).where(Book.id == book_id))

    if not book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not found in MADR',
        )

    return book
