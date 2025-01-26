import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from config import token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()

url = f"https://42f5-178-208-80-247.ngrok-free.app"


@dp.message(Command("support"))
async def cmd_support(message: types.Message):
    await message.answer("Нужна помощь? Вот наши контакты:\nneimark-it.ru")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    btn = InlineKeyboardButton(
        text="НЕЙМАРК.Маркет",
        web_app=WebAppInfo(url=f"{url}/login/{message.from_user.id}/euaugfg87aegf")
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await message.answer("Привет! 🧑‍💻\nЯ – телеграмм-бот мерч-маркета ИТ-кампуса НЕЙМАРК.\nНажми на кнопку чтобы получить крутой мерч 👇", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
