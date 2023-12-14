import time
import asyncio

from aiogram.utils import executor

from Bot.bot 	import Bot_
from Bot.config import Config

from Registers.registers import *



class Main:
    async def on_shutdown():
        await Bot_.send_message(Config.creator_id, "Бот запущен")

    def main():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        executor.start_polling(
            dispatcher   = Bot_.dp,
            skip_updates = True,
            on_shutdown  = loop.run_until_complete(Main.on_shutdown()),
            timeout		 = Bot_.timeout,
        )




if __name__ == "__main__":
	Main.main()
