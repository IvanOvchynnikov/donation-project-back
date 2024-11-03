from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from .utils import decode_token


class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        if not self.token_valid:
            raise HTTPException(status_code=403, detail="Token expired")
        return creds

    @staticmethod
    def token_valid(token: str) -> bool:
        token_data = decode_token(token)
        if token_data is None:
            return False
        return True
