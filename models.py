from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    balance: int
    password: str


class ElectionRoom(BaseModel):
    name: str
    user_id: int
    status: int


class Candidate(BaseModel):
    name: str
    about: str
    election_room_id: int


class Vote(BaseModel):
    user_id: int
    election_room_id: int
    candidate_id: int