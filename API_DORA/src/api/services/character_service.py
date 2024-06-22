from fastapi import HTTPException

from src.api.repositories.base import SQLAlchemyRepository
from src.api.repositories.characters_repo import CharacterRepository
from src.api.repositories.user_repo import UserRepository
from src.api.schemas import CharacterInfo


class CharacterService:
    def __init__(self,
                 character_repo: SQLAlchemyRepository,
                 user_repo: SQLAlchemyRepository):
        self.character_repo: SQLAlchemyRepository() = character_repo
        self.user_repo: SQLAlchemyRepository() = user_repo

    async def add_character(self, user_id: int, character_info: CharacterInfo):
        db_character = await self.character_repo.find_by_options(user_id=user_id, unique=True)
        print(db_character)
        if db_character:
            raise HTTPException(status_code=404, detail="Character exists")
        character_data = {"user_id": user_id, "name": character_info.name, "sex": character_info.sex.value,
                          "age": character_info.age, "model": character_info.model,
                          "path_to_doc": character_info.path_to_doc}

        await self.character_repo.add(data=character_data)

    async def edit_character(self, user_id: int, character_info: CharacterInfo):
        db_character = await self.character_repo.find_by_options(user_id=user_id, unique=True)
        if db_character is None:
            raise HTTPException(status_code=404, detail="Character doesn't exists")
        character_data = {"user_id": user_id, "name": character_info.name, "sex": character_info.sex.value,
                          "age": character_info.age,"model": character_info.model,
                          "path_to_doc": character_info.path_to_doc}

        await self.character_repo.update(data=character_data)
        return "The character has been changed"

    async def delete_character(self, user_id: int):
        db_character = await self.character_repo.find_by_options(user_id=user_id, unique=True)
        if db_character is None:
            raise HTTPException(status_code=404, detail="Character doesn't exists")
        print(db_character.id)
        await self.character_repo.delete_by_options(id_character=db_character.id)
        return "The character has been deleted"


def char_service():
    return CharacterService(character_repo=CharacterRepository(),
                            user_repo=UserRepository())
