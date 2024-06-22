from typing import Annotated
from fastapi import APIRouter, Depends

from src.api.security import get_current_user
from src.api.schemas import User
from src.api.services.request_service import RequestService, req_service

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("/send-request")
async def send_request(message: str,
                       request_service: Annotated[RequestService, Depends(req_service)],
                       user: User = Depends(get_current_user)):
    answer = await request_service.request(user_id=user.id, message=message)

    if answer is not None:
        await request_service.add_history(user_id=user.id, msg_user=message, msg_bot=answer["Response"])
        return answer["Response"]
