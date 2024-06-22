from aiogram import F, Router, Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove

import config
import text
import utils
import db
from doc_vectorization import get_vector_db

dp = Dispatcher(storage=MemoryStorage())
router = Router()
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@router.message(Command("start"))
async def start_handler(msg: Message):
    chat_id = msg.chat.id
    db.create_user(chat_id)
    await msg.answer(text.load_data('greet'), reply_markup=ReplyKeyboardRemove())


@router.message(Command("count_users"))
async def count_handler(msg: Message):
    if msg.chat.id in config.access_list:
        count_users, users = db.count_users()
        await msg.answer('Количество пользователей: ' + str(count_users), reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer(text.load_data('error'), reply_markup=ReplyKeyboardRemove())


@router.message(F.content_type == "text")
async def message_handler(msg: Message):
    chat_id = msg.chat.id
    await bot.send_chat_action(chat_id=msg.chat.id, action="typing")

    answer = utils.rag_run(msg.text, chat_id)
    print(chat_id, answer)
    db.add_text(chat_id, msg.text, answer["Response"])
    await msg.answer(answer["Response"], disable_web_page_preview=True)
