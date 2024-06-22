from src.api.repositories.base import SQLAlchemyRepository
from src.api.db import DBCommunication


class RequestRepository(SQLAlchemyRepository):
    model = DBCommunication
