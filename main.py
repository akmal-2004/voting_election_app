import uvicorn
from models import User
from databases import users

user = User(first_name='Admin', last_name='Admin', email='admin@gmail.com', balance=1000000, username='admin', password='admin')
users.create_user(user.dict())

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
