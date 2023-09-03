from config import *
from .dispatcher import bot
from aiogram.types import FSInputFile
from database.users import get_users_birthday, insert_task, get_user_submit_true, get_chat_id
from datetime import datetime, timedelta
from .modify import draw_image
from .create_message import create_message, make_keyboard
from .chatgpt import chatgpt


async def start_postcards():
    await create_task()
    await send_postcard()


async def create_task():
    if len(result := get_users_birthday()) == 0:
        print('no tasks')
    for item in result:
        # ----
        name = item[0]
        group_id = item[1]
        send_date = datetime.now().date() + timedelta(days=1)
        text_birth = chatgpt(name=name, date=send_date)
        image_path = draw_image(
            text_img=" ".join(item[0].split(" ")[:2]), shad=group_id
        )
        # ----
        id = insert_task(name, group_id, text_birth, send_date, image_path)
        await bot.send_photo(
            photo=FSInputFile(image_path),
            chat_id="-1001951834621",
            caption=create_message(
                stage="basic", name=name, group_id=group_id, text_birth=text_birth, send_date=(datetime.now() + timedelta(days=1)).strftime('%m-%d')),
            reply_markup=make_keyboard(id[0])
        )


async def send_postcard():
    if (users := get_user_submit_true()) == 0:
        return

    for item in users:
        chat_id = get_chat_id(item[1])

        if chat_id is None:
            await bot.send_message(
                chat_id="-1001951834621",
                text="ID беседы не было найдено в базе данных."
            )
        else:
            await bot.send_photo(
                chat_id=chat_id,
                # chat_id='-1001951834621',
                photo=FSInputFile(item[-2]),
                caption=create_message(
                    stage="basic", name=item[1], group_id=item[2], text_birth=item[3], send_date=datetime.now().strftime('%m-%d')
                )
            )
