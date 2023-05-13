from sqlalchemy.ext.asyncio import AsyncSession

import app.models.user as user_model
import app.schemas.user as user_schema


async def create_user(
    db: AsyncSession, user_create: user_schema.UserCreate
) -> user_model.User:
    task = user_model.User(**user_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task