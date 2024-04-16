import os

from fastapi import Depends,status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from jose import jwt,JWTError

from sqlalchemy.orm import Session

# from authx import AuthX,AuthXConfig

from typing import Annotated

from passlib.context import CryptContext
from datetime import timedelta,datetime,timezone

from . import schema
from .import models


pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")
oauth_scheme =  OAuth2PasswordBearer("auth/login")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TIME = 30



# config = AuthXConfig()
# config.JWT_ALGORITHM = ALGORITHM
# config.JWT_SECRET_KEY = SECRET_KEY
# security = AuthX(config=config)



def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(expires_delta)
   
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def decode_token(token):
    return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])


def get_user(token:Annotated[str,Depends(oauth_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:    
        data = decode_token(token)
        return data['sub']
    
    except JWTError as e:
        print(e)
        raise credentials_exception

def get_dbuser(db:Session,userid:int):
    return db.query(models.User).filter(models.User.id == userid).first()


def hash_password(password:str):
    return pwd_context.hash(password) 

def verify_password(plain_password,password):
    return pwd_context.verify(plain_password,password)

def get_me(db:Session,userid:str):
    try:
        user =  get_dbuser(db,userid)
        userdict = {"username":user.username,"email":user.email}
        return userdict
    
    except Exception as e:
        raise HTTPException(status_code=500,detail={"Error":"Sorry Dumb developer didn't know how to handle this error"})


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
                token = create_access_token({"sub":str(user.id)},ACCESS_TIME)
                return {"access_token":token}
        raise HTTPException(status_code=401 ,detail={"Error":"Username or password incorrect"})

    except HTTPException as e:
        raise e
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail={"Error":"Sorry Dumb developer didn't know how to handle this error"})


