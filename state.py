from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from service import *

router = Router()

class AddVacancy(StatesGroup):
    company = State()
    position = State()
    salary = State()
    description = State()
    photo = State()

@router.message(Command("add_vacancy"))
async def add_vacancy(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите название компании:")
    await state.set_state(AddVacancy.company)

@router.message(AddVacancy.company)
async def get_company(message: Message, state: FSMContext):
    if not message.text or not message.text.strip() or message.text.startswith("/"):
        await message.answer("Введите название компании текстом:")
        return

    await state.update_data(company=message.text.strip())
    await message.answer("Введите должность:")
    await state.set_state(AddVacancy.position)

@router.message(AddVacancy.position)
async def get_position(message: Message, state: FSMContext):
    if not message.text or not message.text.strip() or message.text.startswith("/"):
        await message.answer("Введите должность текстом:")
        return

    await state.update_data(position=message.text.strip())
    await message.answer("Введите зарплату в сомони:")
    await state.set_state(AddVacancy.salary)

@router.message(AddVacancy.salary)
async def get_salary(message: Message, state: FSMContext):
    try:
        salary = float(message.text.replace(",", "."))
        if salary <= 0:
            raise ValueError
    except Exception:
        await message.answer("Введите положительную зарплату числом:")
        return

    await state.update_data(salary=salary)
    await message.answer("Напишите описание вакансии:")
    await state.set_state(AddVacancy.description)

@router.message(AddVacancy.description)
async def get_description(message: Message, state: FSMContext):
    if not message.text or not message.text.strip() or message.text.startswith("/"):
        await message.answer("Введите описание текстом:")
        return

    await state.update_data(description=message.text.strip())
    await message.answer("Отправьте фото или логотип компании:")
    await state.set_state(AddVacancy.photo)

@router.message(AddVacancy.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_file_id = message.photo[-1].file_id

    vacancy_id = await create_vacancy(
        message.from_user.id,
        data["company"],
        data["position"],
        data["salary"],
        data["description"],
        photo_file_id
    )

    if vacancy_id:
        await message.answer(f"Вакансия успешно создана! ID: {vacancy_id}")
    else:
        await message.answer("Ошибка при создании вакансии.")

    await state.clear()

@router.message(AddVacancy.photo)
async def wrong_photo(message: Message):
    await message.answer("Отправьте именно фотографию.")