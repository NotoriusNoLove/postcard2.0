from aiogram import Bot, Dispatcher
from config import TOKEN
from aiogram.fsm.strategy import FSMStrategy


bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(fsm_strategy=FSMStrategy.CHAT)
