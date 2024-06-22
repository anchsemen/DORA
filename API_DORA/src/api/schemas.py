from enum import Enum

from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str


class SignInResponse(BaseModel):
    access_token: str
    user_info: User


class Sex(str, Enum):
    Male = "Мужчина"
    Female = "Женщина"


class CharacterInfo(BaseModel):
    name: str
    sex: Sex
    age: int
    path_to_doc: str
    model: str
