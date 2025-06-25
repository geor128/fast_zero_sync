# from django.contrib.auth.models import User
from http import HTTPStatus
from sqlite3 import IntegrityError
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import FilterPage, Message, UserList, UserPublic, UserSchema
from fast_zero.security import (
    get_current_user,
    get_password_hash,
)

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
# app = FastAPI()
router = APIRouter(prefix='/users', tags=['users'])
# criar um banco de dados fake
database = []


# Userlist incluido para remover da lista todos os
# campos que tem password que estiverem nessa lista
# @app.get('/users/', response_model=UserList)
# def read_users(
#     skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
# ):
#     users = session.scalars(select(User).offset(skip).limit(limit)).all()
#     return {'users': users}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
# response_model controla o retorno do que vai aparecer em /docs
def create_user(user: UserSchema, session: Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )  # existe algum User que tem o nome cadastrado?

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        password=hashed_password,
        email=user.email,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/', response_model=UserList)
def read_users(session: Session, filter_users: Annotated[FilterPage, Query()]):
    users = session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    ).all()
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    try:
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return current_user
    except IntegrityError:
        raise HTTPException(
            detail='Username or Email already exists',
            status_code=HTTPStatus.CONFLICT,
        )


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    # db_user = session.scalar(select(User).where(User.id == user_id))

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
