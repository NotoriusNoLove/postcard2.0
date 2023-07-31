from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from aiogram import types
from .callback_datafactory import TestCallbackData


def create_message(stage, name, group_id, text_birth, send_date):
    match stage:
        case "basic":
            return (f"""
<b>👨‍🎓 Имя:</b> <code>{name}</code>
<b>📅 Дата рождения:</b> <code>{str(send_date)[5:] if len(str(send_date)) != 5 else send_date} </code>
<b>🗽 Группа:</b> <code>{group_id} </code>

<b>🎂 Поздравление:</b> <code>{text_birth}</code>
    """)
        case "cancel":
            return (f"""
<b>❌ Отменено </b> <s>

<b>👨‍🎓 Имя:</b> {name}
<b>📅 Дата рождения:</b> {str(send_date)[5:] if len(str(send_date)) != 5 else send_date} 
<b>🗽 Группа:</b> {group_id} 

<b>🎂 Поздравление: {text_birth} </b> </s>
            """)
        case "custom_text":
            return (f""" 
<b>👨‍🎓 Имя:</b> <code>{name}</code>
<b>📅 Дата рождения:</b> <code>{str(send_date)[5:] if len(str(send_date)) != 5 else send_date} </code>
<b>🗽 Группа:</b> <code>{group_id} </code>

<b>🎂 Введите свой текст:</b>
    """)
        case "facts":
            return (f""" 
<b>👨‍🎓 Имя:</b> <code>{name}</code>
<b>📅 Дата рождения:</b> <code>{str(send_date)[5:] if len(str(send_date)) != 5 else send_date} </code>
<b>🗽 Группа:</b> <code>{group_id} </code>

<b>🎂 Введите факты в формате "он любит ..." одним сообщением:</b>
    """)


def make_keyboard(id):
    buttons = [
        [InlineKeyboardButton(
            text="🔄 Перегенерировать", callback_data=TestCallbackData(id=id, event='reg').pack()),
            InlineKeyboardButton(text="❌ Отменить", callback_data=TestCallbackData(
                id=id, event='cancel').pack())],
        [InlineKeyboardButton(
            text="✏️ Свой текст", callback_data=TestCallbackData(id=id, event='custom_text').pack())],
        [InlineKeyboardButton(
            text="➕ Добавить факты", callback_data=TestCallbackData(id=id, event='add_facts').pack()),
            InlineKeyboardButton(text="↔ Выбрать арт", callback_data=TestCallbackData(id=id, event='cancel').pack())]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cancel_keyboard(id):
    buttons = [
        [InlineKeyboardButton(
            text="✅ Восстановить", callback_data=TestCallbackData(id=id, event='recover').pack())]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def make_keyboard_back(id):
    buttons = [
        [InlineKeyboardButton(
            text="⬅ Назад", callback_data=TestCallbackData(id=id, event='recover').pack())]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
