from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from utils import get_hashed_password
from data import create_user, create_todo ,delete_todo ,update_todo ,login_user ,get_todos

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class Todo(BaseModel):
    name: str
    description: str
    uid: int

class Login(BaseModel):
    email: str
    password : str

async def get_user_data(data: UserCreate = Body(...)):
    return {
        'name': data.name,
        'email': data.email,
        'password': data.password,
    }

async def get_todo_data(data: Todo = Body(...)):
    return {
        'name': data.name,
        'description': data.description,
        'uid': data.uid
    } 

@app.post('/signup', summary="Create new user")
async def create_users(user_data: dict = Depends(get_user_data)):
    try:
        return create_user(user_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/post/todo')
async def create_todos(todo_data: dict = Depends(get_todo_data)):
    try:
        return create_todo(todo_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/show_todos")
async def get_all_todos(uid : int):
    try:
        return get_todos(uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/todos/{todo_id}")
async def delete_todo_by_id(todo_id: int):
    try:
        return delete_todo(todo_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/todos/{todo_id}")
async def update_todo_by_id(todo_id: int, todo_data: dict = Depends(get_todo_data)):

    
    return update_todo(todo_id , todo_data)

@app.post("/login")
async def login(data : Login = Body(...)):
    data ={
        "email": data.email,
        "password": data.password
    }
    return login_user(data)
    

