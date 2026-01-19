# Python estándar
import os

from typing import Optional

# Terceros
from fastapi import APIRouter, Body, HTTPException, Query, Request, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

# Proyecto local
from logger import get_logger
from src.database.db_connection import get_db
from src.schemas.user_request import UserCreate
from src.schemas.user_response import UserRead
from src.schemas.token_schemas import Token
from src.services.user_service import create_user_service
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from config import config
from src.authentication.security_service import authenticate_user, create_access_token

router = APIRouter()
logger = get_logger(__name__)


@router.post("/users", response_model=UserRead)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user_service(user_in, db)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
) -> Token:
    
    user = await authenticate_user(db, form_data.username, form_data.password)

  
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
