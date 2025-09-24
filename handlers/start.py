from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from style.messages import start
from keyboard.kb import start_task


start_router = Router()


@start_router.message(Command('start'))
async def start_command(message: Message):
    await message.answer(text=start,
                         parse_mode='HTML',
                         reply_markup=start_task)