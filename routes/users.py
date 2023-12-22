from fastapi import Depends, APIRouter, HTTPException, status
from typing import List, Dict, Any
from databases.users import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)
from models import User
from routes import authentication


router = APIRouter()
PROTECTED = [Depends(authentication.get_current_user)]


@router.post("/", response_model=int, dependencies=PROTECTED)
async def create_user_api(user: User):
    return create_user(user.dict())


@router.get("/{user_id}", dependencies=PROTECTED)
async def get_user_by_id_api(user_id: int):
    user = get_user_by_id(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/", dependencies=PROTECTED)
async def list_users_api():
    return get_all_users()


@router.put("/{user_id}", response_model=bool, dependencies=PROTECTED)
async def update_user_api(user_id: int, updated_data: User):
    updated = update_user(user_id, updated_data.dict())
    if updated:
        return updated
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete("/{user_id}", response_model=bool, dependencies=PROTECTED)
async def delete_user_api(user_id: int):
    deleted = delete_user(user_id)
    if deleted:
        return deleted
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
