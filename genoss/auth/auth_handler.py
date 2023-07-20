from typing import Optional

from fastapi import Header, HTTPException


class AuthHandler:
    @staticmethod
    async def check_auth_header(
        authorization: Optional[str] = Header(None),
    ):
        if authorization is None:
            return None

        components = authorization.split()

        if len(components) != 2 or components[0].lower() != "bearer":
            raise HTTPException(status_code=403, detail="Invalid authorization header")

        api_key = components[1]
        return api_key
