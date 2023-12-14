from aiogram import types

from Accest.translation import tr

from Bot.bot import Bot_

from Handlers.Auth import Auth, FormAuth



Bot_.dp.register_message_handler(
    Auth.start,
    commands = "start",
    state = "*"
)

Bot_.dp.register_message_handler(
    Auth.send_add_data,
    regexp = tr.t2,
    state = "*"
)

Bot_.dp.register_message_handler(
    Auth.add_data,
    content_types = types.ContentType.TEXT,
    state = FormAuth.add_data
)

Bot_.dp.register_message_handler(
    Auth.add_code,
    content_types = types.ContentType.TEXT,
    state = FormAuth.add_code
)

Bot_.dp.register_message_handler(
    Auth.add_password,
    content_types = types.ContentType.TEXT,
    state = FormAuth.add_password
)

Bot_.dp.register_message_handler(
    Auth.add_doner,
    content_types = types.ContentType.TEXT,
    state = FormAuth.add_doner
)

Bot_.dp.register_message_handler(
    Auth.add_channels,
    content_types = types.ContentType.TEXT,
    state = FormAuth.add_channels
)

Bot_.dp.register_message_handler(
    Auth.save_userbot,
    content_types = types.ContentType.TEXT,
    state = FormAuth.save_userbot
)