from aiogram.types import BotCommand

BOT_COMMANDS_LIST = (
    ('start', 'Перезапустить бота'),
    ('suggest', 'Предложить пароль'),
    ('exit', 'Выйти'),
    ('help', 'Помощь')
)

BOT_COMMANDS = [BotCommand(command=name, description=desc)
                for name, desc in BOT_COMMANDS_LIST]

BOT_COMMANDS_STR = '\n'.join('/' + (' - '.join(cmd)) for cmd in BOT_COMMANDS_LIST)
