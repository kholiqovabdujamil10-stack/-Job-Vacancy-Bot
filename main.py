import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from connection import *
from service import *
from state import router as state_router
from callbacks import router as callback_router
from keyboard import *

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start_bot(message: Message):
    await message.answer(
        "Добро пожаловать в Job Vacancy Bot!\n\n"
        "/add_vacancy - создать вакансию\n"
        "/vacancies - список вакансий\n"
        "/vacancy - показать карточку вакансии\n"
        "/my_applications - мои отклики\n"
        "/applicants - список кандидатов\n"
        "/cancel - отменить ввод\n"
        "/help - помощь"
    )


@dp.message(Command("help"))
async def help_bot(message: Message):
    await message.answer(
        "/add_vacancy - создать вакансию\n"
        "/vacancies - показать вакансии\n"
        "/vacancy - показать карточку вакансии\n"
        "/my_applications - мои отклики\n"
        "/applicants - посмотреть кандидатов\n"
        "/cancel - отменить создание вакансии"
    )


@dp.message(Command("vacancies"))
async def vacancies(message: Message):
    vacancies_list = await get_vacancies()

    if not vacancies_list:
        await message.answer("Пока нет открытых вакансий.")
        return

    for vacancy in vacancies_list:
        text = (
            f"Компания: {vacancy['company']}\n"
            f"Должность: {vacancy['position']}\n"
            f"Зарплата: {vacancy['salary']} сомони"
        )

        await message.answer(
            text,
            reply_markup=vacancy_kb(vacancy["id"])
        )


@dp.message(Command("my_applications"))
async def my_applications(message: Message):
    applications = await get_my_applications(message.from_user.id)

    if not applications:
        await message.answer("У вас пока нет откликов.")
        return

    for application in applications:
        await message.answer(
            f"Компания: {application['company']}\n"
            f"Должность: {application['position']}\n"
            f"Статус вакансии: {application['status']}"
        )

@dp.message(Command("vacancy"))
async def vacancy(message: Message):
    vacancies_list = await get_vacancies()

    if not vacancies_list:
        await message.answer("Вакансий пока нет.")
        return

    await message.answer(
        "Выберите вакансию:",
        reply_markup=vacancies_kb(vacancies_list)
    )


@dp.message(Command("applicants"))
async def applicants(message: Message):
    vacancies = await get_my_vacancies(message.from_user.id)

    if not vacancies:
        await message.answer("У вас пока нет вакансий.")
        return

    await message.answer(
        "Выберите вакансию:",
        reply_markup=applicants_kb(vacancies)
    )


@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    if await state.get_state():
        await state.clear()
        await message.answer("Создание вакансии отменено.")
    else:
        await message.answer("Нет активного ввода.")


async def main():
    print("Bot started")
    await create_table()
    dp.include_router(state_router)
    dp.include_router(callback_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())