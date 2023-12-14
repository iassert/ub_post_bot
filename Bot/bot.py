import typing
import logging

from aiogram       import Bot, types
from aiogram.types import base, Message, MessageEntity,\
    InlineKeyboardMarkup, ReplyKeyboardMarkup,\
    ReplyKeyboardRemove, ForceReply

from aiogram.dispatcher                 import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .config import Config

from Log.log import Log

logging.basicConfig(level = logging.INFO)



class Bot_:
    bot: Bot = Bot(token = Config.token)
    dp: Dispatcher = Dispatcher(bot, storage = MemoryStorage())
    
    timeout: int = 300
    sleep: int = 5


    def __init__(self, message: Message):
        self._message: Message = message
    

    async def answer(self,
        text:       base.String,
        parse_mode: typing.Optional[base.String] = "html",
        entities:   typing.Optional[typing.List[MessageEntity]] = None,
        disable_web_page_preview: typing.Optional[base.Boolean] = True,
        disable_notification:     typing.Optional[base.Boolean] = None,
        protect_content:          typing.Optional[base.Boolean] = None,
        allow_sending_without_reply: typing.Optional[base.Boolean] = True,
        reply_markup: typing.Union[
            InlineKeyboardMarkup,
            ReplyKeyboardMarkup,
            ReplyKeyboardRemove,
            ForceReply,
            None,
        ] = None,
        reply: base.Boolean = False
    ) -> Message:
        try:
            return await self._message.answer(
                text,
                parse_mode,
                entities,
                disable_web_page_preview,
                disable_notification,
                protect_content,
                allow_sending_without_reply,
                reply_markup,
                reply
            )
        except BaseException as ex:
            Log("main").error(ex)

    @staticmethod
    async def send_message(
        chat_id:    typing.Union[base.Integer, base.String],
        text:       base.String,
        parse_mode: typing.Optional[base.String] = "html",
        entities:   typing.Optional[typing.List[types.MessageEntity]] = None,
        disable_web_page_preview:    typing.Optional[base.Boolean] = True,
        message_thread_id:           typing.Optional[base.Integer] = None,
        disable_notification:        typing.Optional[base.Boolean] = None,
        protect_content:             typing.Optional[base.Boolean] = None,
        reply_to_message_id:         typing.Optional[base.Integer] = None,
        allow_sending_without_reply: typing.Optional[base.Boolean] = None,
        reply_markup: typing.Union[
            types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, 
            None
        ] = None,
    ) -> types.Message:
        try:
            return await Bot_.bot.send_message(
                chat_id,
                text,
                parse_mode,
                entities,
                disable_web_page_preview,
                message_thread_id,
                disable_notification,
                protect_content,
                reply_to_message_id,
                allow_sending_without_reply,
                reply_markup,
            )
        except BaseException as ex:
            Log("main").error(ex)
   