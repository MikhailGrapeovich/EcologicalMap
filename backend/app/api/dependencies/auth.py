from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.api.dependencies.db import SessionDep
from typing import Annotated
from fastapi import Depends, HTTPException
from app.models.user import User
import jwt
from app.schemas.auth import TokenPayload
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from app.crud.user import get_user
from app.exeptions import IncorrectUsernameOrPasswordException, UserInactiveException, UserNotFound, AuthErrorException, ErrorNoPrivilegesException
from app.utils.auth import ACCESS_TOKEN_ALGORITHM

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")
TokenDep = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(session: SessionDep, token: TokenDep)-> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ACCESS_TOKEN_ALGORITHM)
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise InvalidTokenError
    except(InvalidTokenError, ValidationError):
        raise AuthErrorException
    user = await get_user(session, int(token_data.sub))
    if not user:
        raise UserNotFound
    elif not user.is_active:
        raise UserInactiveException
    return user
CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_current_superuser(current_user: CurrentUser)-> User:
    if not current_user.is_superuser:
        raise ErrorNoPrivilegesException
    return current_user

CurrentSuperUser = Annotated[User, Depends(get_current_user)]