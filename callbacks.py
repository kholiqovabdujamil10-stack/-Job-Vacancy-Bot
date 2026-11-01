# callbacks


from aiogram import Router, F
from aiogram.types import CallbackQuery
from service import *
from keyboard import *

router = Router()

@router.callback_query(F.data.startswith("vacancy_show_"))
async def show_vacancy(callback: CallbackQuery):
    vacancy_id = callback.data.split("_")[-1]
    if int(vacancy_id) <= 0:
        await callback.answer("Неверный ID вакансии", show_alert=True)
        return
    vacancy = await get_vacancy(int(vacancy_id))
    if not vacancy:
        await callback.answer("Вакансия не найдена", show_alert=True)
        return
    text = f"""
Компания: {vacancy['company']}
Должность: {vacancy['position']}
Зарплата: {vacancy['salary']} сомони

Описание: {vacancy['description']}
Статус: {vacancy['status']}
"""
    await callback.message.answer_photo(
        photo=vacancy["photo_file_id"],
        caption=text,
        reply_markup=back_kb(vacancy_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("vacancy_apply_"))
async def apply_vacancy(callback: CallbackQuery):
    vacancy_id = callback.data.split("_")[-1]
    if int(vacancy_id) <= 0:
        await callback.answer("Неверный ID вакансии", show_alert=True)
        return
    result = await create_application(
        callback.from_user.id,
        int(vacancy_id)
    )
    messages = {
        "success": "Вы успешно откликнулись!",
        "exists": "Вы уже откликались!",
        "own": "Нельзя откликаться на свою вакансию!",
        "closed": "Вакансия закрыта!",
        "not_found": "Вакансия не найдена!",
        "error": "Ошибка при отклике!"
    }
    await callback.answer(messages.get(result, "Не удалось выполнить действие"), show_alert=True)


@router.callback_query(F.data.startswith("vacancy_close_"))
async def close_vacancy_callback(callback: CallbackQuery):
    vacancy_id = callback.data.split("_")[-1]
    if int(vacancy_id) <= 0:
        await callback.answer("Неверный ID вакансии", show_alert=True)
        return
    result = await close_vacancy(
        int(vacancy_id),
        callback.from_user.id
    )
    if result:
        await callback.answer("Вакансия закрыта!", show_alert=True)
    else:
        await callback.answer("Вы не автор или вакансия уже закрыта!", show_alert=True)


@router.callback_query(F.data.startswith("vacancy_applicants_"))
async def show_applicants(callback: CallbackQuery):
    vacancy_id = callback.data.split("_")[-1]
    if int(vacancy_id) <= 0:
        await callback.answer("Неверный ID вакансии", show_alert=True)
        return
    users = await get_applicants(
        int(vacancy_id),
        callback.from_user.id
    )
    if users is None:
        await callback.answer("Это не ваша вакансия!", show_alert=True)
        return
    if not users:
        await callback.answer("Откликов пока нет!", show_alert=True)
        return
    text = "Откликнувшиеся пользователи:\n"
    for user in users:
        text += f"\nUser ID: {user['user_id']}"
    await callback.message.answer(text)
    await callback.answer()