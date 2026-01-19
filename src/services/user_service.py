from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from src.models.postgres.user_model import User
from src.schemas.user_request import UserCreate
from src.authentication.security_service import password_hash, get_password_hash
from sqlalchemy.orm import selectinload
from src.models.postgres.user_model import User
from src.models.postgres.role_model import Role


async def create_user_service(user_in: UserCreate, db: AsyncSession) -> User:
    # 1️⃣ Validar si username ya existe
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.username == user_in.username)
    )
    existing_user = result.unique().scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    # 2️⃣ Validar si email ya existe
    if user_in.email:
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.email == user_in.email)
        )
        existing_email = result.unique().scalar_one_or_none()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

    # 3️⃣ Crear usuario
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        disabled=False,
    )

    # 4️⃣ Buscar rol 'user' o crearlo si no existe
    result = await db.execute(select(Role).where(Role.name == "user"))
    role = result.scalar_one_or_none()
    if not role:
        role = Role(name="user", description="Rol por defecto para nuevos usuarios")
        db.add(role)
        await db.commit()
        await db.refresh(role)

    # 5️⃣ Asignar el rol al usuario
    db_user.roles.append(role)

    # 6️⃣ Guardar usuario
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # 7️⃣ Traer usuario nuevamente con roles cargados
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == db_user.id)
    )
    db_user = result.unique().scalar_one_or_none()

    return db_user


