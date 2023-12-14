from Accest.translation import tr

from Bot.bot import Bot_

from Handlers.Post import Post


Bot_.dp.register_message_handler(
    Post.start_userbots,
    regexp = tr.t12,
    state = "*"
)
Bot_.dp.register_message_handler(
    Post.start_del_sys_msg,
    regexp = tr.t26,
    state = "*"
)