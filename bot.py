import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from config import token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()

url = f"https://192.168.52.16:2222"


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    btn = InlineKeyboardButton(text="Открыть мини-приложение",
                               web_app=WebAppInfo(url=f"{url}/login/{message.from_user.id}/euaugfg87aegf")
                               )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await message.answer("Hello!1", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
