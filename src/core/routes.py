from fastapi import APIRouter,HTTPException,Depends,Form
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

from pydantic import AnyUrl
from sqlalchemy.orm import Session
from . import database
from fastapi_filter.base.filter import FilterDepends

from datetime import timedelta

from typing import Annotated

from . import schema,auth,crud

auth_route =  APIRouter(
    prefix="/auth",
    tags=['Auth']
    )

shortner_route = APIRouter(
    prefix="/shorturl",
    tags = ['Url Shortener Dashboard']
    )

short_route = APIRouter()




@auth_route.post('/login')
async def login(db:Annotated[Session,Depends(database.get_db)],user:Annotated[OAuth2PasswordRequestForm,Depends()]):
    print(user)
    return auth.login_user(db,user)

@auth_route.post('/register')
async def register(db:Annotated[Session,Depends(database.get_db)],register_user:schema.UserRegister):
    return auth.register_user(db,register_user)

@auth_route.get('/me') 
async def me(db:Annotated[Session,Depends(database.get_db)],userid:Annotated[str,Depends(auth.get_user)]):
    return auth.get_me(db,userid)

# db:Annotated[Session,Depends(database.get_db)],userid:Annotated[str,Depends(auth.get_user)]
# Url shortner 


    # raise  HTTPException(status_code=400,detail={"error":"This route being developed"})

@shortner_route.get("/urls")
async def all_url(db:Annotated[Session,Depends(database.get_db)],userid:Annotated[str,Depends(auth.get_user)]):
    return crud.get_all_url(db,userid)


@shortner_route.post("/create")
async def create_url(
    db:Annotated[Session,Depends(database.get_db)],
    userid:Annotated[str,Depends(auth.get_user)],
    url:Annotated[AnyUrl,Form()],
    expire_on:Annotated[timedelta,Form()] = None,
    alias:Annotated[str,Form()] = None,
    ):
    urldata = schema.ShortUrl(url=url,alias=alias,expire_on=expire_on)

    return crud.create_shorturl(db,userid,urldata)

@shortner_route.get("/urls/{item_id}")
async def get_url(db:Annotated[Session,Depends(database.get_db)],userid:Annotated[str,Depends(auth.get_user)],item_id:int):
    return crud.get_url_by_id(db,userid,item_id)


@shortner_route.get("/search/")
async def search_url(db:Annotated[Session,Depends(database.get_db)],userid:Annotated[str,Depends(auth.get_user)],search:Annotated[schema.UrlFilter,Depends(schema.UrlFilter)]):
    return crud.search_url(db,userid,search)

@shortner_route.delete("/delete/{item_id}")
async def delete_url(db:Annotated[Session,Depends(database.get_db)],userid:Annotated[str,Depends(auth.get_user)],item_id:int):
    return crud.delete_url_by_id(db,userid,item_id)


@short_route.get("/{url}")
async def redirect_(db:Annotated[Session,Depends(database.get_db)],url:str):
    urlstr =  crud.get_url(db,url)
    return RedirectResponse(urlstr)

