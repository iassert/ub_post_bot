import re

from aiogram            import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from .Auth import Auth

from Accest.markups     import Markups
from Accest.translation import tr

from Bot.bot     import Bot_
from Bot.userbot import UserBot

from Json.json_work import JsonWork



class FormChange(StatesGroup):
    enter_api_id  = State()
    choice_change = State()



class Change:
    async def send_enter_api_id(message: types.Message, state: FSMContext):
        await Bot_(message).answer(tr.t22, reply_markup = Markups.back)
        await FormChange.enter_api_id.set()

    async def enter_api_id(message: types.Message, state: FSMContext):
        if message.text == tr.t3:
            return await Auth.start(message, state)
        
        userbots: dict = JsonWork.read("userbots", {})
        api_id = message.text

        if api_id in userbots:
            userbot  = userbots[api_id]
            api_hash = userbot["api_hash"]

            async with state.proxy() as data:
                data["api_id"]   = api_id
                data["api_hash"] = api_hash
                data["doner_id"] = userbot["doner_id"]
                data["channel_ids"] = userbot["channel_ids"]

            app = UserBot(api_id, api_hash)
            await app.connect()

            return await Change.send_choice_change(message, state)

        await Bot_(message).answer(tr.et15)
        await Change.send_enter_api_id(message, state)

    async def send_choice_change(message: types.Message, state: FSMContext):
        await Bot_(message).answer(tr.t19, reply_markup = Markups.choice)
        await FormChange.choice_change.set()

    async def choice_change(message: types.Message, state: FSMContext):
        if message.text not in tr.bt4:
            return await Bot_(message).answer(tr.et16)
        
        async with state.proxy() as data:
            data["change"] = True
            data["choice"] = message.text

        if message.text == tr.t21:
            return await Auth.send_add_channels(message, state)
        
        await Auth.send_add_doner(message, state)