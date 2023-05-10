from fastapi import APIRouter
from typing import List
import app.schemas.user as user_schema

router = APIRouter()

@router.get("/users", response_model=List[user_schema.User])
async def list_users():
    return [user_schema.User(id=1, name="tom", email="tom@sample.cpm")]

@router.get("/users/{user_id}", response_model=user_schema.User)
async def get_user(user_id: int):
    return user_schema.User(id=user_id, name="tom", email="tom@sample.cpm")

@router.post("/users", response_model=user_schema.UserCreateResponse)
async def create_users(user_body: user_schema.UserCreate):
    return user_schema.UserCreateResponse(id=1, **user_body.dict())

@router.put("/users/{user_id}", response_model=user_schema.UserCreateResponse)
async def update_users(user_id: int, user_body: user_schema.UserCreate):
    return user_schema.UserCreateResponse(id=user_id, **user_body.dict())

@router.delete("/users/{task_id}", response_model=None)
async def delete_users(task_id: int):
    return