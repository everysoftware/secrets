from aiogram.types import BotCommand

BOT_COMMANDS_LIST = (
    ('start', 'Перезапустить бота'),
    ('generate', 'Сгенерировать пароль'),
    ('logout', 'Выйти из аккаунта'),
    ('help', 'Помощь')
)

BOT_COMMANDS = [BotCommand(command=name, description=desc)
                for name, desc in BOT_COMMANDS_LIST]

BOT_COMMANDS_STR = '\n'.join('/' + (' - '.join(cmd)) for cmd in BOT_COMMANDS_LIST)
