from pydantic import BaseModel , EmailStr, conint
from datetime import datetime
from typing import Optional


# request
class UserCreate(BaseModel):
    email:EmailStr
    password:str

# respond schema
class UserOut(BaseModel):
    id : int
    email : str
    created_at : datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id : Optional[int] = None


class BasePost(BaseModel):
    title:str
    content:str
    published:bool = True

class PostCreate(BasePost):
    pass

class Post(BasePost):
    id : int
    title : str
    created_at : datetime
    owner_id : int 
    owner : UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

# vote

class Vote(BaseModel):
    post_id : int
    dir: conint(ge=0, le=1) # type: ignore

