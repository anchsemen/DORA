from fastapi import APIRouter, Depends

from src.api.schemas import User, CharacterInfo
from src.api.services.character_service import CharacterService, char_service
from src.api.security import get_current_user

router = APIRouter(prefix="/characters", tags=["characters"])


@router.post("/init-character")
async def init_character(character_info: CharacterInfo,
                         character_service: CharacterService = Depends(char_service),
                         user: User = Depends(get_current_user)):
    return await character_service.add_character(user_id=user.id, character_info=character_info)


@router.post("/edit-character")
async def edit_character(character_info: CharacterInfo,
                         character_service: CharacterService = Depends(char_service),
                         user: User = Depends(get_current_user)):
    return await character_service.edit_character(user_id=user.id, character_info=character_info)


@router.post("/delete-character")
async def delete_character(character_service: CharacterService = Depends(char_service),
                           user: User = Depends(get_current_user)):
    return await character_service.delete_character(user_id=user.id)
