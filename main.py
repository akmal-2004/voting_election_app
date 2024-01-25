import uvicorn
from models import User
from databases import users
from database import create_connection, create_tables

user = User(first_name='Admin', last_name='Admin', email='admin@gmail.com', balance=1000000, username='admin', password='admin')

if __name__ == "__main__":
    create_tables(create_connection())
    users.create_user(user.dict())
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
