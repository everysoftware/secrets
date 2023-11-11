import inspect
from typing import Callable, Any


class RedirectionCenter:
    def __init__(self):
        self.callback_map: dict[str, Callable] = {}

    def redirect(self, func):
        self.callback_map[func.__name__] = func

        return func

    async def make_redirect_async(self, name: str, **data) -> Any:
        callback = self.callback_map[name]

        sig = inspect.signature(callback)
        args = [param.name for param in sig.parameters.values()]

        return await callback(**{arg: data[arg] for arg in args})


confirmation_center = RedirectionCenter()
