from pydantic import BaseModel, EmailStr


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


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserList(BaseModel):
    users: list[UserPublic]
