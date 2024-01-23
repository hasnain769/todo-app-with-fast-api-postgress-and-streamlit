from models import Users, Base ,Todos
from fastapi import status, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from typing import Dict  # Import the Dict type
from utils import get_hashed_password , verify_password

db_connection_string = "postgresql://syedhasnain769:wpB1eTNEVaU8@ep-delicate-bird-65069304.us-east-2.aws.neon.tech/neondb?sslmode=require"

def create_session():
    engine: Engine = create_engine(db_connection_string, echo=True)
    Session = sessionmaker(bind=engine)
    db: Session = Session()
    return db

def create_user(data: Dict[str, str]):
    db= create_session()
    try:
        existing_user = db.query(Users).filter(Users.email == data['email']).first()
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        new_user = Users(name=data['name'], email=data['email'], password=get_hashed_password(data['password']))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Optional, to ensure we have the latest data in the database

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

    
    return new_user.uid


def create_todo(data :dict[str,str]):
    db = create_session()
    new_Todo= Todos(name=data['name'], description=data['description'], uid=data['uid'])
    db.add(new_Todo)
    db.commit()
    db.close()
    return new_Todo

def get_todos(uid : int ):
    db = create_session()
    todos = db.query(Todos).filter(Todos.uid == uid).all()
    db.close()
    return todos

def delete_todo(id:int):
    db = create_session()
    todo = db.query(Todos).filter(Todos.todo_id== id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    db.close()
    return {"message": "Todo deleted successfully"}

def update_todo(id:int, data:dict[str,str]):
    db = create_session()
    todo = db.query(Todos).filter(Todos.todo_id== id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.name = data['name']
    todo.description = data['description']
    db.commit()
    db.close()
    return todo


def login_user(data : dict[str , str]):
    db = create_session()
    user = db.query(Users).filter(Users.email == data['email']).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data['password'], user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    db.close()

    return user.uid