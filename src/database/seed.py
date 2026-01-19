from sqlalchemy.dialects.postgresql import insert
from src.models.postgres.role_model import Role
import logging
async def seed_roles(conn):
    stmt = insert(Role).values([
        {"name": "admin", "description": "Administrador con todos los permisos"},
        {"name": "user", "description": "Usuario estándar"}
    ]).on_conflict_do_nothing(index_elements=["name"])
    
    result = await conn.execute(stmt)
    logging.info(f"Seed roles executed, inserted rows: {result.rowcount}")
