from fastapi import APIRouter,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from . import database

from typing import Annotated

from . import schema
from . import auth

auth_route =  APIRouter(
    prefix="/auth",
    tags=['Auth']
    )

shortner_route = APIRouter(
    prefix="/url-shortner",
    tags = ['Shortner']
    )




@auth_route.get('/me')
async def me():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})

@auth_route.post('/login')
async def login(db:Annotated[Session,Depends(database.get_db)],user:Annotated[OAuth2PasswordRequestForm,Depends()]):
    return auth.login_user(db,user)

@auth_route.post('/register')
async def register(db:Annotated[Session,Depends(database.get_db)],register_user:schema.UserRegister):
    return auth.register_user(db,register_user)

# Url shortner 

@shortner_route.get("/all")
async def all_url():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})


@shortner_route.get("/get/{item_id}")
async def create_url():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})

@shortner_route.get("/search/")
async def create_url():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})


@shortner_route.post("/create")
async def create_url():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})

@shortner_route.delete("/delete/{item_id}")
async def create_url():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})
