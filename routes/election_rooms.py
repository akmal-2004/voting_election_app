from fastapi import Depends, APIRouter, HTTPException, status
from typing import List, Dict, Any, Optional
from databases.election_rooms import (
    create_election_room,
    create_paid_election_room,
    get_election_room_by_id,
    get_all_election_rooms,
    update_election_room,
    delete_election_room
)
from models import ElectionRoom
from routes import authentication


router = APIRouter()
PROTECTED = [Depends(authentication.get_current_user)]


@router.post("/", response_model=int, dependencies=PROTECTED)
async def create_election_room_api(room: ElectionRoom):
    return create_election_room(room.dict())


@router.post("/paid", dependencies=PROTECTED)
async def create_paid_election_room_api(room: ElectionRoom):
    cost = 50  # The cost to create an election room

    paid_election_room_result = create_paid_election_room(room.dict(), int(cost))

    if paid_election_room_result == True:
        return paid_election_room_result
    else:
        raise HTTPException(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS, detail=paid_election_room_result)


@router.get("/{room_id}", dependencies=PROTECTED)
async def get_election_room_by_id_api(room_id: int):
    room = get_election_room_by_id(room_id)
    if room:
        return room
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Election room not found")


@router.get("/", dependencies=PROTECTED)
async def list_election_rooms_api():
    return get_all_election_rooms()


@router.put("/{room_id}", response_model=bool, dependencies=PROTECTED)
async def update_election_room_api(room_id: int, updated_data: ElectionRoom):
    updated = update_election_room(room_id, updated_data.dict())
    if updated:
        return updated
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Election room not found")


@router.delete("/{room_id}", response_model=bool, dependencies=PROTECTED)
async def delete_election_room_api(room_id: int):
    deleted = delete_election_room(room_id)
    if deleted:
        return deleted
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Election room not found")
