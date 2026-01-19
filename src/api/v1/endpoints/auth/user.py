# Python estándar
import os

from typing import Optional

# Terceros
from fastapi import APIRouter, Body, HTTPException, Query, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

# Proyecto local
from logger import get_logger
from src.database.db_connection import get_db
from src.schemas.user_request import UserCreate
from src.schemas.user_response import UserRead
from src.services.user_service import create_user_service

router = APIRouter()
logger = get_logger(__name__)


@router.post("/users", response_model=UserRead)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user_service(user_in, db)
