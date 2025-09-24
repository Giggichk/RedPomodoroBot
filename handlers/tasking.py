import asyncio
import random
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from style.messages import time
from keyboard.kb import chooice_time, stop_button
from state.states import PomodoroState


task_router = Router()


async def pomodoro(user_id: int, bot, cycles: int, state: FSMContext):
    try:
        await state.set_state(PomodoroState.working)

        for i in range(1, cycles + 1):
            await bot.send_message(user_id, text=random.choice(["🌿", "🍀", "🌱"]))
            await bot.send_message(user_id, text=f"🌿 Начался {i} цикл:\n"
                                        f"Сейчас работаем 25 минут, упорно достигаем своей цели!🪴"
            )
            await asyncio.sleep(25 * 60)

            if i <= cycles:
                await bot.send_message(user_id, text="Отлично, у нас отдых 5 минут🍅")
                await asyncio.sleep(5 * 60)

        await bot.send_message(user_id, text="Поздравляю, ты успешно поработал!")
        await bot.send_message(user_id, text=random.choice(["👍", "😁", "🫶"]))
    except asyncio.CancelledError:
        await bot.send_message(user_id, text="⛔ Pomodoro остановлен!")
    finally:
        await state.clear()
        await state.update_data(pomodoro_task=None)


async def start_pomodoro(callback: CallbackQuery, state: FSMContext, cycles: int, text: str):
    await callback.answer()
    await callback.message.delete()
    data = await state.get_data()
    if data.get("pomodoro_task"):
        await callback.message.answer("⏳ Pomodoro уже запущен. Дождись окончания или останови!")
        return

    task = asyncio.create_task(pomodoro(callback.from_user.id, callback.message.bot, cycles, state))
    await state.update_data(pomodoro_task=task)
    await callback.message.answer(text, reply_markup=stop_button)


@task_router.callback_query(F.data == "tasking")
async def task_process(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    if await state.get_state() == PomodoroState.working:
        await callback.message.bot.send_message(
            callback.from_user.id,
            "⏳ У тебя уже запущен Pomodoro. Дождись окончания!"
        )
        return

    await callback.message.bot.send_message(
        callback.from_user.id,
        text=time,
        parse_mode='HTML',
        reply_markup=chooice_time
    )


@task_router.callback_query(F.data == "30")
async def task_30(callback: CallbackQuery, state: FSMContext):
    await start_pomodoro(callback, state, 1, "🔗 Запускаю Pomodoro на 30 минут!\n\n"
                                                        "Рекомендуем убрать уведомления и другие отвлекающие факторы⚠️")


@task_router.callback_query(F.data == "1")
async def task_60(callback: CallbackQuery, state: FSMContext):
    await start_pomodoro(callback, state, 2, "🔗 Запускаю Pomodoro на 1 час!\n\n"
                                                         "Рекомендуем убрать уведомления и другие отвлекающие факторы⚠️")


@task_router.callback_query(F.data == "1.5")
async def task_90(callback: CallbackQuery, state: FSMContext):
    await start_pomodoro(callback, state, 3, "🔗 Запускаю Pomodoro на 1.5 часа!\n\n"
                                             "Рекомендуем убрать уведомления и другие отвлекающие факторы⚠️")


@task_router.callback_query(F.data == "2")
async def task_120(callback: CallbackQuery, state: FSMContext):
    await start_pomodoro(callback, state, 4, "🔗 Запускаю Pomodoro на 2 часа!\n\n"
                                             "Рекомендуем убрать уведомления и другие отвлекающие факторы⚠️")


@task_router.message(F.text == "Прекратить")
async def stop_pomodoro(message: Message, state: FSMContext):
    data = await state.get_data()
    task: asyncio.Task = data.get("pomodoro_task")

    if task and not task.done():
        task.cancel()
    else:
        await message.answer("❌ У тебя сейчас нет активного Pomodoro.")