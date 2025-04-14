from http import HTTPStatus

# from django.contrib.auth.models import User
from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()
# criar um banco de dados fake
database = []

# @app.get('/', status_code=HTTPStatus.OK)
# def read_root():
#     return {'message': 'Olá Mundo!'}


@app.get('/users/{user_id}')
def read_root(user_id: int):
    if user_id == 1:
        return {'message': 'Olá Joba!'}


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
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
# response_model controla o retorno do que vai aparecer em /docs
def create_user(user: UserSchema):
    # breakpoint() # para debugar entre 127.0.0.1/docs e clica em
    # execute e para exibir digite l e para sair digite q
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)
    return user_with_id


# Userlist incluido para remover da lista todos os
# campos que tem password que estiverem nessa lista
@app.get('/users', response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    del database[user_id - 1]
    return {'message': 'User deleted'}
