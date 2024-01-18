from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from utils import get_hashed_password
from data import create_user, create_todo

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class Todo(BaseModel):
    name: str
    description: str
    uid: int

async def get_user_data(data: UserCreate = Body(...)):
    return {
        'name': data.name,
        'email': data.email,
        'password': get_hashed_password(data.password),
    }

async def get_todo_data(data: Todo = Body(...)):
    return {
        'name': data.name,
        'description': data.description,
        'uid': data.uid
    } dummyP@ssword1234

@app.post('/signup', summary="Create new user")
async def create_users(user_data: dict = Depends(get_user_data)):
    try:
        return create_user(user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/post/todo')
async def create_todo(todo_data: dict = Depends(get_todo_data)):
    try:
        create_todo(todo_data)
        return {"message": "Todo created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
