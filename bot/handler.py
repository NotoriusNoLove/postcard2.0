from .dispatcher import dp
# from callback_func import regeneration_callback, cancel_callback, recover_callback, custom_text_callback, begin
from .callback import *
from .callback_datafactory import TestCallbackData
from aiogram import F


def register_handlers():
    dp.callback_query.register(
        regeneration_callback, TestCallbackData.filter(F.event == "reg"))
    dp.callback_query.register(
        cancel_callback, TestCallbackData.filter(F.event == "cancel"))
    dp.callback_query.register(
        recover_callback, TestCallbackData.filter(F.event == "recover"))
    dp.callback_query.register(
        custom_text_callback, TestCallbackData.filter(F.event == "custom_text"))
    dp.callback_query.register(
        add_facts, TestCallbackData.filter(F.event == "add_facts"))
