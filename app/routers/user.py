from fastapi import APIRouter, Depends
from typing import List
import app.schemas.user as user_schema
from sqlalchemy.ext.asyncio import AsyncSession

import app.cruds.user as user_crud
from app.db import get_db

router = APIRouter()


@router.get("/users", response_model=List[user_schema.User])
async def list_users():
    return [user_schema.User(id=1, name="tom", email="tom@sample.cpm")]


@router.get("/users/{user_id}", response_model=user_schema.User)
async def get_user(user_id: int):
    return user_schema.User(id=user_id, name="tom", email="tom@sample.cpm")


@router.post("/tasks", response_model=user_schema.UserCreateResponse)
async def create_task(
    user_body: user_schema.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_crud.create_user(db, user_body)


@router.put("/users/{user_id}", response_model=user_schema.UserCreateResponse)
async def update_users(user_id: int, user_body: user_schema.UserCreate):
    return user_schema.UserCreateResponse(id=user_id, **user_body.dict())


@router.delete("/users/{task_id}", response_model=None)
async def delete_users(task_id: int):
    return