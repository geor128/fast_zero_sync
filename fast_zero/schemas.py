from pydantic import BaseModel, ConfigDict, EmailStr


# controla que apenas mensagem responde, caso passe outro parametro ele rejeita
# ate se mudar o tipo
class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


"""
 O Pydantic, por padrão, não sabe como lidar com os modelos do SQLAlchemy, o que nos leva ao erro observado nos testes.

A solução para esse problema é fazer uma alteração no esquema UserPublic que utilizamos, para que ele possa reconhecer e trabalhar com os modelos do SQLAlchemy. Isso permite a conversão direta de objetos do SQLAlchemy em esquemas Pydantic.

Para isso, adicionaremos a linha model_config = ConfigDict(from_attributes=True) ao nosso esquema:
"""


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str

class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100
