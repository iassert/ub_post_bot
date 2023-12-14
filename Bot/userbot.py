import os

from pyrogram        import Client
from pyrogram.errors import SessionPasswordNeeded, UserAlreadyParticipant
from pyrogram.types  import User, Message, MessageEntity
from pyrogram.enums  import ChatMemberStatus

from Log.log import Log


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, name: str | int, *args):
        name = str(name)

        if name not in cls._instances:
            instance = super().__call__(name, *args)
            cls._instances[name] = instance
        return cls._instances[name]
    

class UserBot(metaclass = SingletonMeta):
    def __init__(self, 
        name: str | int, 
        api_id_: int | str = 2040, 
        api_hash_: str = "b18441a1ff607e10a989891a5462e627"
    ):
        self._name = str(name)
        self._api_id   = api_id_
        self._api_hash = api_hash_
        self._is_start = False
        self._app = None

    async def connect(self) -> bool:
        try:
            if self._app is None:
                self._app = Client(self.path(), self._api_id, self._api_hash)
                await self._app.connect()
                Log(self._name).info("connect")
            
            return True
        except UserAlreadyParticipant as ex:
            return True
        except Exception as ex:
            Log(self._name).error(ex)
        return False

    def path(self):
        dir_ = os.path.dirname(os.path.realpath(__file__))
        dir_ = os.path.dirname(dir_)

        session_dir = os.path.join(dir_, "session")

        if not os.path.exists(session_dir):
            os.mkdir(session_dir)

        return os.path.join(session_dir, self._name)

    async def phone(self, phone_: str) -> bool:
        try:
            self._phone = phone_
            self._sent_code = await self._app.send_code(phone_)
            Log(self._name).info("{phone_}: send code")

            return True
        except Exception as ex:
            Log(self._name).error(ex)
        return False

    async def code(self, code_: str) -> int:
        try:
            signed_in = await self._app.sign_in(self._phone, self._sent_code.phone_code_hash, code_)
            
            if isinstance(signed_in, User):
                Log(self._name).info("add")
                return 0
        except SessionPasswordNeeded:
            Log(self._name).info("need password")
            return 1
        except Exception as ex:
            Log(self._name).error(ex)
        return 2
    
    async def password(self, password: str) -> bool:
        try:
            await self._app.check_password(password)
            Log(self._name).info("app: password is correct")

            return True
        except Exception as ex:
            Log(self._name).error(ex)
        return False
    
    async def join(self, link: str) -> int | None:
        try:
            chat = await self._app.join_chat(link)
            return chat.id
        except UserAlreadyParticipant as ex:
            Log(self._name).error(ex)

            chat = await self._app.get_chat(link)
            return chat.id
        except Exception as ex:
            Log(self._name).error(ex)

    async def get_chat(self, chat_id: int | str) -> bool:
        try:
            chat_member = await self._app.get_chat_member(chat_id, "me")

            return chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
        except Exception as ex:
            Log(self._name).error(ex)
        return False
    
    async def first_name(self) -> str:
        try:
            me_ = await self._app.get_me()
            return me_.first_name
        except Exception as ex:
            Log(self._name).error(ex)
        return ""

    async def get_chat_history(self, chat_id: int, limit: int = -1) -> list[Message]:
        messages: list[Message] = []

        try:
            i = -1
            async for j in self._app.get_chat_history(chat_id):
                message: Message = j

                type_ = UserBot.message_type(message)
                if type_ is None:
                    continue
                messages.append(message)

                if i == limit:
                    break
                i += 1

        except Exception as ex:
            Log(self._name).error(ex)

        return messages[::-1]

    async def get_messages(self, chat_id: int, messages_id: list[int] | int) -> list[Message] | Message | None:
        try:
            return await self._app.get_messages(chat_id, messages_id)
        except Exception as ex:
            Log(self._name).error(ex)


    async def send_video_note(self,
        chat_id: int, 
        video_note_id: str
    ) -> Message | None:
        try:
            return await self._app.send_video_note(
                chat_id,
                video_note_id
            )
        except Exception as ex:
            Log(self._name).error(ex)

    async def send_video(self,
        chat_id: int,
        video_id: int,
        caption: str,
        caption_entities: MessageEntity
    ) -> Message | None:
        try:
            return await self._app.send_video(
                chat_id,
                video_id,
                caption = caption,
                caption_entities = caption_entities
            )
        except Exception as ex:
            Log(self._name).error(ex)

    async def send_photo(self,
        chat_id: int,
        photo_id: int,
        caption: str,
        caption_entities: MessageEntity
    ) -> Message | None:
        try:
            return await self._app.send_photo(
                chat_id,
                photo_id,
                caption = caption,
                caption_entities = caption_entities
            )
        except Exception as ex:
            Log(self._name).error(ex)

    async def send_message(self,
        chat_id: int,
        text: str
    ) -> Message | None:
        try:
            return await self._app.send_message(
                chat_id,
                text
            )
        except Exception as ex:
            Log(self._name).error(ex)


    def message_type(message: Message) -> str | None:
        if message.media_group_id:
            return 

        if message.video_note:
            return "video_note"
        
        if message.video:
            return "video"
        
        if message.photo:
            return "photo"
        
        if message.text:
            return "text"
