"""
This will hand schema for application [pydantic]
"""
from pydantic import BaseModel,EmailStr

"""
User Schema real
"""


class User(BaseModel):
    username : str

class RetriveUser(User):
    email:EmailStr

class UserRegister(RetriveUser):
    password: str

class LoginUser(User):
    password:str

