from fastapi import FastAPI
from models import User, ElectionRoom
from sqlite_database import create_connection, create_tables
from routes.users import router as users_router
from routes.election_rooms import router as election_rooms_router
from routes.candidates import router as candidates_router
from routes.votes import router as votes_router
from routes.authentication import router as authentication_router

app = FastAPI()

# Create database connection and tables
conn = create_connection()
create_tables(conn)
conn.close()

# Mount routers
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(election_rooms_router, prefix="/api/election-rooms", tags=["election_rooms"])
app.include_router(candidates_router, prefix="/api/candidates", tags=["candidates"])
app.include_router(votes_router, prefix="/api/votes", tags=["votes"])
app.include_router(authentication_router, prefix="/api/auth", tags=["auth"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
