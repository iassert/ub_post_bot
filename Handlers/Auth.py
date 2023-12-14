import re

from aiogram            import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Accest.markups     import Markups
from Accest.translation import tr

from Bot.bot     import Bot_
from Bot.userbot import UserBot

from Json.json_work import JsonWork



class FormAuth(StatesGroup):
    add_data = State()
    add_code     = State()
    add_password = State()

    add_doner    = State()
    add_channels = State()

    save_userbot = State()



class Auth:
    # = 0 - /start
    async def start(message: types.Message, state: FSMContext):
        await Bot_(message).answer(tr.t1, reply_markup = Markups.start)
        await state.finish()
    
    # -> 1
    async def send_add_data(message: types.Message, state: FSMContext):
        await Bot_(message).answer(tr.t24, reply_markup = Markups.back)
        await FormAuth.add_data.set()
    

    # = 1
    # 0 <-
    # -> 2
    async def add_data(message: types.Message, state: FSMContext):
        if message.text == tr.t3:
            return await Auth.start(message, state)
        
        data = message.text.split('\n')
        len_data = len(data)

        if len_data != 4:
            t = tr.et18
            if len_data > 4:
                t = tr.et17

            await Bot_(message).answer(t)
            return await Auth.send_add_data(message, state)
        
        phone, password, doner_id, channel_ids = data
        
        last_id = 0
        userbots = JsonWork.read("userbots", {})
        if userbots:
            last_id = int([*userbots.keys()][-1]) + 1

        app = UserBot(last_id)

        if not await app.connect():
            await Bot_(message).answer(tr.et3)
            return await Auth.send_add_data(message, state)

        if not await app.phone(phone):
            await Bot_(message).answer(tr.et4)
            return Auth.send_add_data(message, state)
        
        async with state.proxy() as data:
            data["last_id"] = last_id
            data["phone"] = phone
            data["password"] = password
            data["doner_id"] = doner_id
            data["channel_ids"] = channel_ids

        await Auth.send_add_code(message, state)


    # -> 2
    async def send_add_code(message: types.Message, state: FSMContext):
        await Bot_(message).answer(tr.t7)
        await FormAuth.add_code.set()

    # = 2
    # 1 <- 
    # 3 <- 
    # -> 4 -> 5 -> 6
    async def add_code(message: types.Message, state: FSMContext):
        if message.text == tr.t3:
            return await Auth.send_add_data(message, state)
        
        async with state.proxy() as data:
            last_id = data["last_id"]
            password = data["password"]
            doner_id = data["doner_id"]
            channel_ids = data["channel_ids"]

        app = UserBot(last_id)
        state_code = await app.code(message.text)

        if state_code == 2:
            await Bot_(message).answer(tr.et6)
            return await Bot_(message).answer(tr.t7)
        
        if state_code == 1:
            if not await app.password(password):
                await Bot_(message).answer(tr.et7)
                await Bot_(message).answer(tr.t8)
                return await FormAuth.add_password.set()
    
        #finish
        
        if not await Auth.header_doner(message, state, doner_id):
            return
        
        if not await Auth.header_channels(message, state, channel_ids):
            return
        
        await Auth.send_save_userbot(message, state)


    # = 3
    async def add_password(message: types.Message, state: FSMContext):
        if message.text == tr.t3:
            return await Auth.send_add_code(message, state)
        
        async with state.proxy() as data:
            last_id  = data["last_id"]
            doner_id = data["doner_id"]
            channel_ids = data["channel_ids"]

        app = UserBot(last_id)
        if not await app.password(message.text):
            await Bot_(message).answer(tr.et7)
            return await Bot_(message).answer(tr.t8)

        if not await Auth.header_doner(message, state, doner_id):
            return
        
        if not await Auth.header_channels(message, state, channel_ids):
            return
        
        await Auth.send_save_userbot(message, state)


    # -> 4
    async def send_add_doner(message: types.Message, state: FSMContext):
        await Bot_(message).answer(tr.t10, reply_markup = Markups.back)
        await FormAuth.add_doner.set()

    # = 4
    async def add_doner(message: types.Message, state: FSMContext):
        if message.text == tr.t3:
            return await Auth.send_add_code(message, state)

        if not await Auth.header_doner(message, state, message.text):
            return
        
        async with state.proxy() as data:
            channel_ids = data["channel_ids"]
    
        if not await Auth.header_channels(message, state, channel_ids):
            return
        
        await Auth.send_save_userbot(message, state)

    # - 4
    async def header_doner(message: types.Message, state: FSMContext, doner: str) -> bool:
        async with state.proxy() as data:
            last_id  = data["last_id"]

        app = UserBot(last_id)
        if doner[:5] == "https":
            doner_id = await app.join(doner)
        elif doner[:4] == "-100":
            doner_id = int(doner)
        else:
            await Bot_(message).answer(tr.et8)
            return False

        if doner_id is None:
            await Bot_(message).answer(tr.et9)
            return False

        if not await app.get_chat(doner_id):
            await Bot_(message).answer(tr.et10)
            return False
        
        async with state.proxy() as data:
            data["doner_id"] = doner_id

        return True
    

    # -> 5
    async def send_add_channels(message: types.Message, state: FSMContext):
        await Bot_(message).answer(tr.t11, reply_markup = Markups.back)
        await FormAuth.add_channels.set()

    # = 5
    async def add_channels(message: types.Message, state: FSMContext):
        if message.text == tr.t3:
            return await Auth.send_add_code(message, state)

        if not await Auth.header_channels(message, state, message.text):
            return
        
        await Auth.send_save_userbot(message, state)

    # - 5
    async def header_channels(message: types.Message, state: FSMContext, channels: str) -> bool:
        async with state.proxy() as data:
            last_id  = data["last_id"]

        app = UserBot(last_id)

        if channels[:5] == "https":
            channel_ids = []

            for i in channels.split():
                chat_id = await app.join(i)

                if chat_id is None:
                    await Bot_(message).answer(tr.et11.format(i))
                    continue

                channel_ids.append(chat_id)

        elif channels[:4] == "-100":
            channel_ids = []

            for i in channels.split():
                i = int(i)

                if not await app.get_chat(i):
                    await Bot_(message).answer(tr.et13.format(i))
                    continue

                channel_ids.append(i)
        else:
            await Bot_(message).answer(tr.et19)
            return False

        if not channel_ids:
            await Bot_(message).answer(tr.et12)
            return False

        async with state.proxy() as data:
            data["channel_ids"] = channel_ids

        return True
    

    # -> 6
    async def send_save_userbot(message: types.Message, state: FSMContext):
        await Bot_(message).answer(tr.t15, reply_markup = Markups.q)
        await FormAuth.save_userbot.set()

    # = 6
    async def save_userbot(message: types.Message, state: FSMContext):
        if message.text not in tr.bt3:
            return await Bot_(message).answer(tr.et14)
        
        async with state.proxy() as data:
            last_id  = data["last_id"]
            doner_id = data["doner_id"]
            channel_ids = data["channel_ids"]
        
        await state.finish()
        if message.text == tr.t17:
            return await Bot_(message).answer(tr.t25, reply_markup = Markups.start)

        app = UserBot(last_id)
        userbots: dict = JsonWork.read("userbots", {})
        userbots[last_id] = {
            "api_id": app._api_id,
            "api_hash": app._api_hash,
            "doner_id": doner_id,
            "channel_ids": channel_ids,
        }
        JsonWork.write("userbots", userbots)

        await Bot_(message).answer(tr.t9, reply_markup = Markups.start)
        await Bot_(message).answer(tr.t23.format(last_id))
