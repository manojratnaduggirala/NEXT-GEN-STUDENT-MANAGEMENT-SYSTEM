from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(title="NextGenSMS API")

# Example Pydantic models
class User(BaseModel):
    id: int
    username: str
    email: str
    role: str

# Dummy data for demonstration
users_db = [
    {"id": 1, "username": "admin1", "email": "admin1@example.com", "role": "admin"},
    {"id": 2, "username": "student1", "email": "student1@example.com", "role": "student"},
    {"id": 3, "username": "teacher1", "email": "teacher1@example.com", "role": "teacher"},
]

@app.get("/users/", response_model=List[User])
async def get_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# To run FastAPI app:
# uvicorn next_gen_sms.api_views:app --reload --port 8001

if __name__ == "__main__":
    uvicorn.run("next_gen_sms.api_views:app", host="0.0.0.0", port=8001, reload=True)
