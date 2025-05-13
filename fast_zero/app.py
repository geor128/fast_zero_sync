
# from django.contrib.auth.models import User
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, Token, UserList, UserPublic, UserSchema
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI()
# criar um banco de dados fake
database = []

# @app.get('/', status_code=HTTPStatus.OK)
# def read_root():
#     return {'message': 'Olá Mundo!'}


# @app.get('/users/{user_id}')
# def read_root(user_id: int):
#     if user_id == 1:
#         return {'message': 'Olá Joba!'}


# @app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
# def read_root():
#     return """
#     <html>
#     <head>
#     <title>FastZero nosso olá mundo</title>
#     </head>
#     <body>
#         <h1>FastZero nosso mundo</h1>
#     </body>
#     </html>"""


# ...

# criar um novo teste para verificar se o nosso endpoint
# está retornando o usuário correto quando existe um usuário no banco
def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


@app.get(
    '/', status_code=HTTPStatus.OK, response_model=Message
)  # formalizando um contrato formalizando uma resposta
def read_root1():
    return {'message': 'Olá Mundo!'}


@app.get(
    '/resposta/{sexo}', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def read_root2(sexo: str):
    if sexo == 'm':
        return """
        <html>
        <head>
            <title>O sexo masculino</title>
        </head>
        <body>
            <h1>O sexo masculino</h1>
        </body>
        </html>
        """
    elif sexo == 'f':
        return """
            <html>
            <head>
                <title>O sexo feminino</title>
            </head>
            <body>
                <h1>O sexo feminino</h1>
            </body>
            </html>
        """


@app.get('/exercicio-html', response_class=HTMLResponse)
def exercicio_aula_02():
    return """
    <html>
      <head>
        <title>Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""


# response_class
# @app.post('/users/',status_code=HTTPStatus.CREATED,response_model=UserPublic)
# #response_model controla o retorno do que vai aparecer em /docs
# @app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
# response_model controla o retorno do que vai aparecer em /docs
# def create_user(user: UserSchema):
# breakpoint() # para debugar entre 127.0.0.1/docs e clica em
# execute e para exibir digite l e para sair digite q
 # user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
 # database.append(user_with_id)
 #  return user_with_id


# Userlist incluido para remover da lista todos os
# campos que tem password que estiverem nessa lista
@app.get('/users/', response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


# ...

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)
    return current_user
    


''' db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    try:
        db_user.username = user.username
        db_user.password = get_password_hash(user.password)
        db_user.email = user.email
        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists'
        )'''


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    ):
    # db_user = session.scalar(select(User).where(User.id == user_id))

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user__exercicio(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return database[user_id - 1]


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
# response_model controla o retorno do que vai aparecer em /docs
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
            )
    )  # existe algum User que tem o nome cadastrado?

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Username already exists'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Email already exists'
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


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
