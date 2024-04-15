from sqlalchemy.orm import Session
from authx import AuthX,AuthXConfig
from . import schema
from .import models
from fastapi import HTTPException


from passlib.context import CryptContext


import os

config = AuthXConfig()
config.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

security = AuthX(config=config)


pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")


def hash_password(password:str):
    return pwd_context.hash(password) 

def verify_password(plain_password,password):
    return pwd_context.verify(plain_password,password)

def register_user(db:Session,user:schema.UserRegister):
    try:    
        new_user  =  models.User(username =user.username,email = user.email,password = hash_password(user.password))
     
        if db.query(models.User).filter(models.User.username == new_user.username).first() is not None:
            raise HTTPException(status_code=400,detail={"error":"Username is already taken please choose another"})

        if db.query(models.User).filter(models.User.email == new_user.email).first() is not None:
            raise HTTPException(status_code=400,detail={"error":"Email is already taken please choose another"})

        db.add(new_user)
        db.commit()

        return {"success":"User created succesfully"}
    
    except HTTPException as e:
        raise e
        
    except Exception as e:
        raise HTTPException(status_code=500,detail={"error":"error while creating user"})
    
def login_user(db:Session,login_details:schema.LoginUser):
    try:
        user =  db.query(models.User).filter(models.User.username == login_details.username).first()
     
        if user:
            if verify_password(login_details.password,user.password):
                token = security.create_access_token(uid=str(user.id)) 
                return {"access_token":token}
        raise HTTPException(status_code=401 ,detail={"Error":"Username or password incorrect"})

    except HTTPException as e:
        raise e
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail={"Error":"Sorry Dumb developer didn't know how to handle this error"})


