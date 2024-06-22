from fastapi import HTTPException

from src.api.repositories.base import SQLAlchemyRepository
from src.api.repositories.requests_repo import RequestRepository
from src.api.repositories.user_repo import UserRepository
from src.api.tasks.make_request import run_model


class RequestService:
    def __init__(self,
                 request_repo: SQLAlchemyRepository,
                 user_repo: SQLAlchemyRepository):
        self.request_repo: SQLAlchemyRepository() = request_repo
        self.user_repo: SQLAlchemyRepository() = user_repo

    async def add_history(self, user_id: int, msg_user: str, msg_bot: str):
        db_request = await self.request_repo.find_by_options(user_id=user_id, unique=True)
        if db_request is None:
            history_user = msg_user
            history_bot = msg_bot
            request_data = {"user_id": user_id,
                            "user_msg": history_user, "bot_msg": history_bot}
            await self.request_repo.add(data=request_data)
        else:
            history_user = f"{db_request.user_msg} | {msg_user}" \
                if db_request.user_msg and db_request.bot_msg else msg_user
            history_bot = f"{db_request.bot_msg} | {msg_bot}" \
                if db_request.user_msg and db_request.bot_msg else msg_bot
            request_data = {"user_id": user_id,
                            "user_msg": history_user, "bot_msg": history_bot}
            await self.request_repo.update(data=request_data)

    async def request(self, user_id: int, message: str):
        db_request = await self.request_repo.find_by_options(user_id=user_id, unique=True)
        history = ''
        if db_request is not None:
            if db_request.user_msg and db_request.bot_msg:
                history_user = db_request.user_msg.split('|')[-5:]
                history_bot = db_request.bot_msg.split('|')[-5:]
                combined_history = list(zip(history_user, history_bot))
                history = ''.join(
                    [f'Пользователь: {user_msg}; БОТ {bot_msg}' for user_msg, bot_msg in combined_history])

        data_to_update = run_model(message, history)
        if data_to_update["is_success"]:
            return data_to_update["output_data"]
        else:
            raise HTTPException(
                status_code=404, detail=f"Error in predict: {data_to_update['error_info']}   ")


def req_service():
    return RequestService(request_repo=RequestRepository(),
                          user_repo=UserRepository())
