import re
import asyncio

from aiogram            import types
from aiogram.dispatcher import FSMContext

from pyrogram.types import Message

from Accest.translation import tr

from Bot.bot     import Bot_
from Bot.config  import Config
from Bot.userbot import UserBot

from Json.json_work import JsonWork

from Log.log import Log

from datetime import datetime, timedelta



class Post:
    async def start_del_sys_msg(mesage: types.Message, state: FSMContext):
        userbots: dict = JsonWork.read("userbots", {})
        for last_id, userbot in userbots.items():
            api_id   = userbot["api_id"]
            api_hash = userbot["api_hash"]
            channel_ids = userbot["channel_ids"]

            app = UserBot(last_id, api_id, api_hash)
            if app._app is None and not await app.connect():
                continue

            asyncio.create_task(Post.del_sys_msg(app, channel_ids))

            await Bot_(mesage).answer(tr.t14.format(last_id, await app.first_name()))
        await Bot_(mesage).answer(tr.t27)

    async def del_sys_msg(app: UserBot, channel_ids: list[int]):
        for channel_id in channel_ids:
            async for msg in app._app.get_chat_history(channel_id):
                msg: Message
                if not msg.service:
                    continue

                try:
                    await msg.delete()
                except BaseException as ex:
                    Log("main").error(ex)


    async def start_userbots(mesage: types.Message, state: FSMContext):
        await Bot_(mesage).answer(tr.t13)

        userbots: dict = JsonWork.read("userbots", {})
        for last_id, userbot in userbots.items():
            api_id   = userbot["api_id"]
            api_hash = userbot["api_hash"]
            doner_id = userbot["doner_id"]
            channel_ids = userbot["channel_ids"]

            app = UserBot(last_id, api_id, api_hash)
            if app._is_start:
                continue

            if app._app is None and not await app.connect():
                continue
            
            asyncio.create_task(Post.cycle(app, doner_id, channel_ids))

            app._is_start = True
            await Bot_(mesage).answer(tr.t14.format(last_id, await app.first_name()))
        await Bot_(mesage).answer(tr.t27)

    async def cycle(app: UserBot, doner_id: int, channel_ids: list[int], update_date: datetime = None):
        if update_date is None:
            update_date = Post._to_date(Post._sdate() + Config.post_update_time)

        wait = (update_date - datetime.now()).total_seconds()
        await asyncio.sleep(wait)

        messages = await app.get_chat_history(doner_id, Config.limit)
    
        for time_, message in zip(Config.post_times, messages):
            for channel_id in channel_ids:
                type_ = UserBot.message_type(message)
                l = Log("main")
                l.info(f"app_id:{app._api_id}\n{type_}:{channel_id},{message.id}\n{time_}\n")

                Post.send_post(app, doner_id, channel_id, message, time_)

        await Post.cycle(app, doner_id, channel_ids, update_date + timedelta(days = 1))

    def send_post(app: UserBot, doner_id: int, chat_id: int, message: Message, time_: str):
        async def _send_post(app: UserBot, doner_id: int, chat_id: int, message: Message, time_: str):
            date_post = Post._to_date(Post._sdate() + time_)

            wait = (date_post - datetime.now()).total_seconds()
            if wait <= 0:
                return
            
            await asyncio.sleep(wait)

            msg = None
            message = await app.get_messages(doner_id, message.id)

            if not message:
                return

            if message.video_note:
                msg = await app.send_video_note(
                    chat_id,
                    message.video_note.file_id
                )
            elif message.video:
                msg = await app.send_video(
                    chat_id, 
                    message.video.file_id, 
                    caption = message.caption, 
                    caption_entities = message.caption_entities
                )
            elif message.photo:
                msg = await app.send_photo(
                    chat_id, 
                    message.photo.file_id, 
                    caption = message.caption, 
                    caption_entities = message.caption_entities
                )
            elif message.text:
                msg = await app.send_message(
                    chat_id, 
                    message.text.html
                )

            if not msg:
                return
            
            date_reset_1 = Post._to_date(Post._sdate() + Config.reset_time_1)
            date_reset_2 = Post._to_date(Post._sdate() + Config.reset_time_2)
            
            wait_1 = int((date_reset_1 - date_post).total_seconds())
            wait_2 = int((date_reset_2 - date_post).total_seconds())
            wait = wait_1 if wait_1 > 0 else wait_2

            await asyncio.sleep(wait)

            try:
                await msg.delete()
            except BaseException as ex:
                Log("main").error(ex)

        asyncio.create_task(_send_post(app, doner_id, chat_id, message, time_))
        

    def _sdate() -> str:
        return datetime.now().strftime("%d.%m.%Y ")

    def _to_date(sdatetime: str) -> datetime:
        return datetime.strptime(sdatetime, "%d.%m.%Y %H:%M")