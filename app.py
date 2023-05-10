# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=import-error
# pylint: disable=too-few-public-methods
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from db.db import get_password, insert_password, delete_password, add_user, check_user 
from worker import delete_message
import asyncio

load_dotenv()


class GetForm(StatesGroup):
    service = State()


class DelForm(StatesGroup):
    service = State()


class SetForm(StatesGroup):
    service = State()
    login = State()
    password = State()


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


#start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    if not check_user(user_id):
        print("no user in db")
        add_user(message.from_user.id)
    print(message.from_user.id)
    await message.reply(message.from_user.id)


#get password
@dp.message_handler(commands=['get'], state=None)
async def start_get_command(message: types.Message):
    await GetForm.service.set()
    await message.reply("Напиши название сервиса")

@dp.message_handler(state=GetForm.service)
async def get_command(message: types.Message, state: FSMContext):
    async with state.proxy():
        user_id = message.from_user.id
        service_name = message.text.lower()
        data = get_password(user_id, service_name)
        if not data :
            await message.reply("Нет сохраненных паролей для данного сервиса")
        else:
            msg = await message.reply(data)
            asyncio.create_task(delete_message(msg, 60))
    await state.finish()


#set password
@dp.message_handler(commands=['set'], state=None)
async def start_set_command(message: types.Message):
    await SetForm.service.set()
    await message.reply("Напиши название сервиса")

@dp.message_handler(state=SetForm.service)
async def service_set_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['service'] = message.text.lower()
    await SetForm.next()
    await message.reply('Напишите логин')

@dp.message_handler(state=SetForm.login)
async def login_set_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    await SetForm.next()
    await message.reply('Напишите пароль, сообщение с паролем удалится через 30 сек')

@dp.message_handler(state=SetForm.password)
async def password_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
        asyncio.create_task(delete_message(message, 60))
        user_id = message.from_user.id
        insert_password(user_id, data['service'], data['login'], data['password'])
        print(data['service'], data['login'])
        await message.reply('Пароль создан')
    await state.finish()


#del password
@dp.message_handler(commands=['del'], state=None)
async def start_del_command(message: types.Message):
    await DelForm.service.set()
    await message.reply("Напиши название сервиса")

@dp.message_handler(state=DelForm.service)
async def del_command(message: types.Message, state: FSMContext):
    async with state.proxy():
        user_id = message.from_user.id
        service_name = message.text.lower()
        success = delete_password(user_id, service_name)
        if success:
            await message.reply("Пароль удален")
        else:
            await message.reply("Нет сохраненных паролей для данного сервиса")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
