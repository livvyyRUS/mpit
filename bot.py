import asyncio
import json
import logging
import os

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from config import token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()

TOKEN = "0F8ofm1AYuuCiIU9uimnq4fnqsm7905zacLkeEmC2rDLgAYVYwsIE9fgAUPNaagQ"

url = f"https://fe43-178-208-80-247.ngrok-free.app"
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


@dp.message(Command("activate"))
async def cmd_activate(message: types.Message):
    response = requests.get(f"{api_url}/admins")
    if message.from_user.id not in response.json().get("data"):
        return
    try:
        data = int(message.text.split(" ", maxsplit=1)[1].strip())
    except:
        await message.answer("Что-то пошло не так")
        return
    response = requests.post(f"{api_url}/register", data=json.dumps({
        "token": TOKEN,
        "user_id": data
    }))
    if response.status_code == 200:
        await message.answer("Успешно")
        return
    await message.answer("Что-то пошло не так")


@dp.message(Command("change_points"))
async def cmd_change_points(message: types.Message):
    response = requests.get(f"{api_url}/admins")
    if message.from_user.id not in response.json().get("data"):
        return
    try:
        _, data, pts = message.text.split(" ", maxsplit=2)
        data = int(data.strip())
        pts = int(pts.strip())
    except:
        await message.answer("Что-то пошло не так")
        return

    response = requests.post(f"{api_url}/change_points", data=json.dumps({
        "user_id": data,
        "points": pts
    }))
    print(response.text)
    if response.status_code == 200:
        await message.answer("Успешно")
        return
    await message.answer("Что-то пошло не так")


@dp.message(Command("add_product"))
async def add_product(message: types.Message):
    try:
        text = message.caption.split(' ', 2)
        print(message.text)
        name = text[1]
        price = int(text[2])
        numb = len(os.listdir('src/products'))
        file_name = f'src/products/{numb}.jpg'
        await bot.download(message.photo[-1], destination=file_name)
    except Exception as e:
        print(e)
        await message.answer('Что-то пошло не так')
        return

    response = requests.post(f"{api_url}/products/add", data=json.dumps({
        "token": TOKEN,
        "data": [
            {
                "product_id": numb,
                "name": name,
                "image": f"{numb}.jpg",
                "price": price
            }
        ]
    }))
    if response.status_code == 200:
        await message.answer("Успешно")
        return
    await message.answer("Что-то пошло не так")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
