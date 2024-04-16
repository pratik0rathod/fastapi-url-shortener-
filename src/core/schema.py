"""
This will hand schema for application [pydantic]
"""
from pydantic import BaseModel,EmailStr,AnyUrl
from datetime import datetime,timedelta
from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional
from . import models

"""
User Schema real
"""

class UrlFilter(Filter):

    url__like:Optional[str] = None

    class Constants(Filter.Constants):
        model = models.ShortUrls
        search_field_name = "search"
        search_model_fields =["url"]


class User(BaseModel):
    username : str

class RetriveUser(User):
    email:EmailStr

class UserRegister(RetriveUser):
    password: str

class LoginUser(User):
    password:str


class ShortUrl(BaseModel):
    url:AnyUrl
    alias:str | None
    expire_on:timedelta | None = timedelta.max

class RetriveShortUrl(ShortUrl):
    total_clicks:int 
    created_on:datetime
    
