from src.api.repositories.base import SQLAlchemyRepository
from src.api.db import DBUser


class UserRepository(SQLAlchemyRepository):
    model = DBUser
