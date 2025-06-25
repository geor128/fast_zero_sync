# from django.contrib.auth.models import User
from http import HTTPStatus

from fastapi import FastAPI
from starlette.responses import HTMLResponse

from fast_zero.routers import auth, users
from fast_zero.schemas import Message, UserPublic

app = FastAPI(title='AGTECCORE')
app.include_router(auth.router)
app.include_router(users.router)
# criar um banco de dados fake


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
