import inspect
from typing import Callable, Any


class CallbackManager:
    callback_map: dict[int, Callable]

    def __init__(self):
        self.callback_map = {}

    def callback(self, func):
        self.callback_map[hash(func)] = func

        return func

    async def invoke(self, redirect_hash: int, **data) -> Any:
        if redirect_hash not in self.callback_map:
            raise ValueError(f"Callback {redirect_hash} not found")

        f = self.callback_map[redirect_hash]
        sig = inspect.signature(f)
        args = [param.name for param in sig.parameters.values()]

        return await f(**{arg: data[arg] for arg in args})


manager = CallbackManager()
