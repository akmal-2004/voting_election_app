from fastapi import Depends, APIRouter, HTTPException, status
from typing import List, Dict, Any
from databases.candidates import (
    create_candidate,
    get_candidate_by_id,
    get_all_candidates,
    update_candidate,
    delete_candidate
)
from models import Candidate
from routes import authentication


router = APIRouter()
PROTECTED = [Depends(authentication.get_current_user)]

@router.post("/", response_model=int, dependencies=PROTECTED)
async def create_candidate_api(candidate: Candidate):
    return create_candidate(candidate.dict())


@router.get("/{candidate_id}", dependencies=PROTECTED)
async def get_candidate_by_id_api(candidate_id: int):
    candidate = get_candidate_by_id(candidate_id)
    if candidate:
        return candidate
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")


@router.get("/", dependencies=PROTECTED)
async def list_candidates_api():
    return get_all_candidates()


@router.put("/{candidate_id}", response_model=bool, dependencies=PROTECTED)
async def update_candidate_api(candidate_id: int, updated_data: Candidate):
    updated = update_candidate(candidate_id, updated_data.dict())
    if updated:
        return updated
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")


@router.delete("/{candidate_id}", response_model=bool, dependencies=PROTECTED)
async def delete_candidate_api(candidate_id: int):
    deleted = delete_candidate(candidate_id)
    if deleted:
        return deleted
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
