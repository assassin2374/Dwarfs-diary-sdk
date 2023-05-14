from fastapi import FastAPI, Depends, HTTPException
from .db import SessionLocal
from typing import List
from . import models, schemas
from app.routers import user

# FastAPIのアプリケーションオブジェクトを作成する
app = FastAPI()

app.include_router(user.router)

@router.post("/tasks", response_model=schemas.UserCreateResponse)
async def create_task(
    task_body: user_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    return await task_crud.create_task(db, task_body)