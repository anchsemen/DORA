from src.api.repositories.base import SQLAlchemyRepository
from src.api.db import DBCharacters


class CharacterRepository(SQLAlchemyRepository):
    model = DBCharacters
