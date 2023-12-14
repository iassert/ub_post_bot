from aiogram import types

from Accest.translation import tr

from Bot.bot import Bot_

from Handlers.Change import Change, FormChange



"""
Bot_.dp.register_message_handler(
    Change.send_enter_api_id,
    regexp = tr.t18,
    state = "*"
)

Bot_.dp.register_message_handler(
    Change.enter_api_id,
    content_types = types.ContentTypes.TEXT,
    state = FormChange.enter_api_id
)

Bot_.dp.register_message_handler(
    Change.choice_change,
    content_types = types.ContentTypes.TEXT,
    state = FormChange.choice_change
)
"""