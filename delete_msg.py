# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=import-error
# pylint: disable=too-few-public-methods
import os
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))

async def delete_msg(chat_id, msg_id):
    await bot.delete_message(chat_id, msg_id)
