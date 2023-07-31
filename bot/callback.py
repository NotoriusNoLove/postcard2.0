from aiogram import types
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from .callback_datafactory import TestCallbackData
from database.engine import conn, cur
from .create_message import create_message, make_keyboard, cancel_keyboard, make_keyboard_back
from .dispatcher import bot
from .chatgpt import chatgpt
form_router = Router()


class Form(StatesGroup):
    custom_start = State()
    add_facts = State()


async def regeneration_callback(call: types.CallbackQuery, callback_data: TestCallbackData):
    cur.execute(
        f"""
        SELECT * FROM TASKS
        WHERE id = {callback_data.id} 
    """
    )
    result: tuple = cur.fetchone()  # type: ignore
    cur.execute(
        f"""
        UPDATE tasks
            SET text_birth = '{chatgpt(name=result[1], date=result[4])}'
            WHERE id = {callback_data.id} 
            RETURNING *;
        """
    )
    conn.commit()
    result: tuple = cur.fetchone()  # type: ignore
    await call.message.edit_caption(    # type: ignore
        caption=create_message(
            stage="basic", name=result[1], group_id=result[2], text_birth=result[3], send_date=result[4]
        ),
        reply_markup=make_keyboard(result[0])
    )


async def cancel_callback(call: types.CallbackQuery, callback_data: TestCallbackData):
    # меняем submit на false
    cur.execute(
        f"""UPDATE tasks
        SET submit = False
        WHERE id = {callback_data.id}
        RETURNING *;
        """
    )
    result: tuple = cur.fetchone()  # type: ignore
    conn.commit()
    await call.message.edit_caption(        # type: ignore
        caption=create_message(
            stage="cancel", name=result[1], group_id=result[2], text_birth=result[3], send_date=result[4]
        ),
        reply_markup=cancel_keyboard(result[0])
    )


async def recover_callback(call: types.CallbackQuery, callback_data: TestCallbackData):
    # меняем submit на true
    cur.execute(
        f"""UPDATE tasks
        SET submit = True
        WHERE id = {callback_data.id}
        RETURNING *;
        """
    )
    result: tuple = cur.fetchone()  # type: ignore
    conn.commit()
    await call.message.edit_caption(        # type: ignore
        caption=create_message(
            stage="basic", name=result[1], group_id=result[2], text_birth=result[3], send_date=result[4]
        ),
        reply_markup=make_keyboard(result[0])
    )


async def custom_text_callback(call: types.CallbackQuery, callback_data: TestCallbackData, state: FSMContext):
    cur.execute(
        f"""select * from tasks
            where id = {callback_data.id}"""
    )
    result: tuple = cur.fetchone()  # type: ignore
    await call.message.edit_caption(  # type: ignore
        caption=create_message(
            stage="custom_text", name=result[1], group_id=result[2], text_birth=result[3], send_date=result[4]
        ),
        reply_markup=make_keyboard_back(result[0])
    )
    await state.set_state(Form.custom_start)
    await state.update_data(result=result, callback_data=callback_data, call=call)


@form_router.message(Form.custom_start)
async def custom_text(message: Message, state: FSMContext):
    data = await state.get_data()
    cur.execute(
        f"""UPDATE tasks
        SET text_birth = '{message.text}'
        WHERE id = {data['callback_data'].id};
        """
    )
    conn.commit()
    await data['call'].message.edit_caption(
        caption=create_message(
            stage="basic", name=data['result'][1], group_id=data['result'][2], text_birth=message.text, send_date=data['result'][4]
        ),
        reply_markup=make_keyboard(data['result'][0])
    )
    await message.delete()
    await state.clear()


async def add_facts(call: types.CallbackQuery, callback_data: TestCallbackData, state: FSMContext):
    cur.execute(
        f"""select * from tasks
            where id = {callback_data.id}"""
    )
    result: tuple = cur.fetchone()  # type: ignore
    await call.message.edit_caption(  # type: ignore
        caption=create_message(
            stage="facts", name=result[1], group_id=result[2], text_birth=result[3], send_date=result[4]
        ),
        reply_markup=make_keyboard_back(result[0])
    )
    await state.set_state(Form.add_facts)
    await state.update_data(result=result, callback_data=callback_data, call=call)


@form_router.message(Form.add_facts)
async def custom_text(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    text_birth = chatgpt(data['result'][1], data['result'][4], message.text)
    cur.execute(
        f"""UPDATE tasks
        SET text_birth = '{text_birth}'
        WHERE id = {data['callback_data'].id}
        RETURNING *;
        """
    )
    conn.commit()
    result: tuple = cur.fetchone()  # type: ignore
    await data['call'].message.edit_caption(
        caption=create_message(
            stage="basic", name=result[1], group_id=result[2], text_birth=text_birth, send_date=result[4]
        ),
        reply_markup=make_keyboard(data['result'][0])
    )
    await state.clear()
