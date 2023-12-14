from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from .translation import tr


class Markups:
    def markup(bt: list[list[str]] | list[str] | str | int = None) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard = True)
        if bt is None:
            return markup
        
        if isinstance(bt, str | int):
            bt = [bt]

        if isinstance(bt[0], str | int):
            bt = [bt]

        for i in bt:
            markup.row(*[KeyboardButton(j) for j in i])
        return markup

    start  = markup(tr.bt1)
    back   = markup(tr.bt2)
    q      = markup(tr.bt3)
    choice = markup(tr.bt4)