import asyncio
import json
import logging

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from config import token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()

url = f"https://58f4-178-208-80-247.ngrok-free.app"
api_url = 'http://localhost:12345'


def create_user(user_id: int):
    response = requests.post(f"{api_url}/create_user_if_not_exists", data=json.dumps({"user_id": user_id}))
    print(response.text)


def get_token(user_id: int):
    response = requests.get(f"{api_url}/get_token", data=json.dumps({"user_id": user_id}))
    return response.text.strip('"')


@dp.message(Command("support"))
async def cmd_support(message: types.Message):
    create_user(message.from_user.id)
    await message.answer("Нужна помощь? Вот наши контакты:\nneimark-it.ru")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    create_user(message.from_user.id)
    _token = get_token(message.from_user.id)
    print(f"{url}/login/{message.from_user.id}/{_token}")
    btn = InlineKeyboardButton(
        text="НЕЙМАРК.Маркет",
        web_app=WebAppInfo(url=f"{url}/login/{message.from_user.id}/{_token}")
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await message.answer(
        "Привет! 🧑‍💻\nЯ – телеграмм-бот мерч-маркета ИТ-кампуса НЕЙМАРК.\nНажми на кнопку чтобы получить крутой мерч 👇",
        reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
