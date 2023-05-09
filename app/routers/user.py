from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def list_users():
    pass

@router.get("/users/{user_id}")
async def get_user():
    pass

@router.post("/users")
async def create_users():
    pass

@router.put("/users/{user_id}")
async def update_users():
    pass

@router.delete("/users/{task_id}")
async def delete_users():
    pass