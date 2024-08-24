from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import User
from madr.schemas import Message, UserList, UserPublic, UserSchema
from madr.security import get_password_hash

router = APIRouter(prefix='/users', tags=['users'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    user_db = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    if user_db:
        if user_db.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username já consta no MADR',
            )
        if user_db.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email já consta no MADR',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(session: T_Session, skip: int = 0, limit: int = 50):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: T_Session):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não consta no MADR',
        )

    if session.scalar(
        select(User).where(User.username == user.username, User.id != user_id)
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username já consta no MADR',
        )

    if session.scalar(
        select(User).where(User.email == user.email, User.id != user_id)
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Email já consta no MADR',
        )

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = get_password_hash(user.password)

    session.commit()
    session.refresh(user_db)

    return user_db


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(user_id: int, session: T_Session):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não consta no MADR',
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
