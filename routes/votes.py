from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from databases.votes import (
    create_vote,
    get_vote_by_id,
    get_all_votes,
    update_vote,
    delete_vote
)
from models import Vote


router = APIRouter()


@router.post("/", response_model=int)
async def create_vote_api(vote: Vote):
    return create_vote(vote.dict())


@router.get("/{vote_id}")
async def get_vote_by_id_api(vote_id: int):
    vote = get_vote_by_id(vote_id)
    if vote:
        return vote
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")


@router.get("/")
async def list_votes_api():
    return get_all_votes()


@router.put("/{vote_id}", response_model=bool)
async def update_vote_api(vote_id: int, updated_data: Vote):
    updated = update_vote(vote_id, updated_data.dict())
    if updated:
        return updated
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")


@router.delete("/{vote_id}", response_model=bool)
async def delete_vote_api(vote_id: int):
    deleted = delete_vote(vote_id)
    if deleted:
        return deleted
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
