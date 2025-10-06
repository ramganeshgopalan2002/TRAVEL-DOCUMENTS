from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="My API", version="1.0.0")

# Pydantic model for data validation
class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

# In-memory storage (use database in production)
users_db = []

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to My API", "status": "active"}

@app.get("/users")
async def get_users():
    return {"users": users_db}

@app.post("/users")
async def create_user(user: User):
    users_db.append(user.dict())
    return {"message": "User created", "user": user}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if 0 <= user_id < len(users_db):
        return users_db[user_id]
    return {"error": "User not found"}

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    if 0 <= user_id < len(users_db):
        users_db[user_id] = user.dict()
        return {"message": "User updated", "user": user}
    return {"error": "User not found"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if 0 <= user_id < len(users_db):
        deleted_user = users_db.pop(user_id)
        return {"message": "User deleted", "user": deleted_user}
    return {"error": "User not found"}