from typing import Optional

import jwt
from fastapi_users import models, BaseUserManager, exceptions
from fastapi_users.authentication import JWTStrategy, Strategy
from fastapi_users.jwt import generate_jwt, decode_jwt


class SecondStrategy(Strategy):
    pass


class JWTSecondStrategy(SecondStrategy, JWTStrategy[models.UP, models.ID]):
    async def read_token(
        self, token: Optional[str], user_manager: BaseUserManager[models.UP, models.ID]
    ) -> Optional[models.UP]:
        if token is None:
            return None

        try:
            data = decode_jwt(
                token, self.decode_key, self.token_audience, algorithms=[self.algorithm]
            )
            user_id = data.get("sub")
            if user_id is None or not data.get("two_fa"):
                return None
        except jwt.PyJWTError:
            return None

        try:
            parsed_id = user_manager.parse_id(user_id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID):
            return None

    async def write_token(self, user: models.UP) -> str:
        data = {"sub": str(user.id), "aud": self.token_audience, "two_fa": True}
        return generate_jwt(
            data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm
        )
