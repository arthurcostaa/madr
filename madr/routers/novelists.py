from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Novelist, User
from madr.schemas import NovelistPublic, NovelistSchema
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
