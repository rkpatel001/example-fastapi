from fastapi import FastAPI , Response , status , HTTPException , Depends
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

from random import randrange

from . import models , schema , utils
from app.database import engine , get_db
from passlib.context import CryptContext
from app.routers import post , user , auth , vote
from .config import settings

# sqlalchemy
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {"message" : "Hello welcome to my api"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)






