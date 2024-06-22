from aiogram import F, Router, Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, CallbackQuery, InputMediaPhoto, InputFile
from aiogram.client.bot import DefaultBotProperties

import config
import db
import kb
import text
import utils


dp = Dispatcher(storage=MemoryStorage())
router = Router()
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@router.message(Command("start"))
async def start_handler(msg: Message):
    chat_id = msg.chat.id
    db.create_user(chat_id)
    await msg.answer(text.start_message)
    photo = FSInputFile("photos/MEGAN.png")
    await bot.send_photo(chat_id=chat_id, photo=photo)


@router.message(Command("count_users"))
async def count_handler(msg: Message):
    if msg.chat.id in config.access_list:
        count_users, users = db.count_users()
        await msg.answer('Количество пользователей: ' + str(count_users), reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer(text.error, reply_markup=ReplyKeyboardRemove())


@router.callback_query(F.data == "buy")
async def roofs_trip(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    await callback.message.answer('Thanks! Enjoy my photo', reply_markup=ReplyKeyboardRemove())
    media = [
        InputMediaPhoto(media=FSInputFile('photos/naked/MEGAN1.png'), caption='Photo 1'),
        InputMediaPhoto(media=FSInputFile('photos/naked/MEGAN2.png'), caption='Photo 2'),
        InputMediaPhoto(media=FSInputFile('photos/naked/MEGAN3.png'), caption='Photo 3'),
        InputMediaPhoto(media=FSInputFile('photos/naked/MEGAN4.png'), caption='Photo 4')
    ]

    await bot.send_media_group(chat_id=chat_id, media=media)


@router.message(F.content_type == "text")
async def message_handler(msg: Message):
    await bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    chat_id = msg.chat.id
    if db.check_user(chat_id):
        previous_message, len_history = db.get_inf(chat_id)
        if len_history % 10 == 0:
            last_10_mes = db.get_last_10_entries(chat_id)
            nsfw_class = await utils.nsfw_class(last_10_mes + [msg.text])
            if nsfw_class:
                answer = await utils.generate_response(msg.text, previous_message)
                db.add_text(chat_id, msg.text, answer)
                await msg.answer(answer, disable_web_page_preview=True)
                photo = FSInputFile("photos/all_blur.png")
                await bot.send_photo(chat_id=chat_id, photo=photo, caption=text.buy_prompt, reply_markup=kb.buy)
            else:
                classificator_photo = await utils.classifier_text(msg.text)
                if classificator_photo:
                    answer = await utils.generate_response(msg.text, previous_message)
                    db.add_text(chat_id, msg.text, answer)
                    await msg.answer(answer, disable_web_page_preview=True)
                    photo = FSInputFile("photos/all_blur.png")
                    await bot.send_photo(chat_id=chat_id, photo=photo, caption=text.buy_prompt, reply_markup=kb.buy)
                else:
                    answer = await utils.generate_response(msg.text, previous_message)
                    db.add_text(chat_id, msg.text, answer)
                    await msg.answer(answer, disable_web_page_preview=True)
        else:
            classificator_photo = await utils.classifier_text(msg.text)
            if classificator_photo:
                answer = await utils.generate_response(msg.text, previous_message)
                db.add_text(chat_id, msg.text, answer)
                await msg.answer(answer, disable_web_page_preview=True)
                photo = FSInputFile("photos/all_blur.png")
                await bot.send_photo(chat_id=chat_id, photo=photo, caption=text.buy_prompt, reply_markup=kb.buy)
            else:
                answer = await utils.generate_response(msg.text, previous_message)
                db.add_text(chat_id, msg.text, answer)
                await msg.answer(answer, disable_web_page_preview=True)
