from database_schema import Users, Base ,Todos
from fastapi import status, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from typing import Dict  # Import the Dict type

db_connection_string = "postgresql://syedhasnain769:wpB1eTNEVaU8@ep-delicate-bird-65069304.us-east-2.aws.neon.tech/neondb?sslmode=require"

def create_session():
    engine: Engine = create_engine(db_connection_string, echo=True)
    Session = sessionmaker(bind=engine)
    db: Session = Session()
    return db

def create_user(data: Dict[str, str]):
    db = create_session()
    existing_user = db.query(Users).filter(Users.email == data['email']).first()
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create a new user instance and add it to the session
    new_user = Users(name=data['name'], email=data['email'], password=data['password'])
    db.add(new_user)

    # Commit the changes to the database
    db.commit()

    # Optionally, you might want to return some response
    return {"message": "User created successfully"}


def create_todo(data :dict[str,str]):
    db = create_session()
    new_Todo= Todos(name=data['name'], description=data['description'], uid=data['uid'])
    db.add(new_Todo)


