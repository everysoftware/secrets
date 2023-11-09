from unittest.mock import AsyncMock

import pytest

from bot.handlers.commands import BOT_COMMANDS_STR
from bot.handlers.start import author, help_


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'handler, expected_text',
    [
        (help_, '<b>Способности бота:</b>\n\n' + BOT_COMMANDS_STR),
        (author, 'Разработчик бота: @ivanstasevich 👨‍💻')
    ]
)
async def test_easy_handlers(handler, expected_text):
    msg = AsyncMock()
    await handler(msg)
    msg.answer.assert_awaited_with(expected_text)
