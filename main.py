import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.start import start_router
from handlers.tasking import task_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(start_router, task_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Осуществлен выход.')