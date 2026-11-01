from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def applicants_kb(vacancies):
    buttons = []
    for vacancy in vacancies:
        buttons.append([InlineKeyboardButton(text=vacancy["position"], callback_data=f"vacancy_applicants_{vacancy['id']}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def vacancies_kb(vacancies):
    buttons = []
    for vacancy in vacancies:
        buttons.append([InlineKeyboardButton(text=vacancy["position"], callback_data=f"vacancy_show_{vacancy['id']}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def vacancy_kb(vacancy_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подробнее", callback_data=f"vacancy_show_{vacancy_id}"),
            InlineKeyboardButton(text="📩 Откликнуться", callback_data=f"vacancy_apply_{vacancy_id}")],

            [InlineKeyboardButton(text="🔒 Закрыть", callback_data=f"vacancy_close_{vacancy_id}")]
        ]
    )

def back_kb(vacancy_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📩 Откликнуться", callback_data=f"vacancy_apply_{vacancy_id}")]
        ]
    )