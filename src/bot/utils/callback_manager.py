import inspect
from typing import Any, Callable


class CallbackManager:
    callback_map: dict[int, tuple[Callable, tuple[str]]]

    def __init__(self):
        self.callback_map = {}

    def callback(self, func):
        sig = inspect.signature(func)
        args = tuple(param.name for param in sig.parameters.values())
        self.callback_map[hash(func)] = func, args

        return func

    async def invoke(self, redirect_hash: int, **data) -> Any:
        if redirect_hash not in self.callback_map:
            raise ValueError(f"Callback {redirect_hash} not found")

        f, args = self.callback_map[redirect_hash]
        return await f(**{arg: data[arg] for arg in args})


manager = CallbackManager()
