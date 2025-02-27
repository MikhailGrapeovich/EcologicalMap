from app.api.dependencies.db import SessionDep
from app.config import settings
from fastapi import APIRouter, Depends
from app.schemas.auth import Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.crud.user import authenticate
from app.exeptions import IncorrectUsernameOrPasswordException, UserInactiveException
from datetime import timedelta
from app.utils.auth import create_access_token


router = APIRouter()

@router.post("/login/access-token")
async def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate(session, form_data.username, form_data.password)
    if not user:
        raise IncorrectUsernameOrPasswordException
    elif not user.is_active:
        raise UserInactiveException
    access_token_expiration = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(access_token = create_access_token(user.id, access_token_expiration))