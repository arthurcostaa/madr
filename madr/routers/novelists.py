from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Novelist, User
from madr.schemas import Message, NovelistPublic, NovelistSchema
from madr.security import get_current_user
from madr.utils import sanitize

router = APIRouter(prefix='/novelists', tags=['novelists'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=NovelistPublic
)
def create_novelist(
    novelist: NovelistSchema, session: T_Session, user: T_CurrentUser
):
    novelist_db = session.scalar(
        select(Novelist).where(Novelist.name == sanitize(novelist.name))
    )

    if novelist_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Novelist already exists.',
        )

    db_novelist = Novelist(name=sanitize(novelist.name))

    session.add(db_novelist)
    session.commit()
    session.refresh(db_novelist)

    return db_novelist


@router.delete(
    '/{novelist_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_novelist(novelist_id: int, session: T_Session, user: T_CurrentUser):
    novelist_db = session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )

    if not novelist_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Novelist not found in MADR',
        )

    session.delete(novelist_db)
    session.commit()

    return {'message': 'Novelist deleted from MADR'}


@router.patch(
    '/{novelist_id}', status_code=HTTPStatus.OK, response_model=NovelistPublic
)
def update_novelist(
    novelist_id: int,
    novelist: NovelistSchema,
    session: T_Session,
    user: T_CurrentUser,
):
    novelist_db = session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )

    if not novelist_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Novelist not found in MADR',
        )

    try:
        novelist_db.name = sanitize(novelist.name)
        session.commit()
        session.refresh(novelist_db)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Novelist already exists in MADR',
        )

    return novelist_db
