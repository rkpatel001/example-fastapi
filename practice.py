from fastapi import FastAPI,Body
from pydantic import BaseModel,EmailStr
from random import randrange


app = FastAPI()


class Posts(BaseModel):
    name : str
    age : int = 20
    email : EmailStr

my_post_data = [{"name" : "Ronak" , "age" : 18, "email" : "ronka@gmail.com" , "id" : 1},{"name" : "Rk" , "age" : 20, "email" : "rk@gmail.com" , "id" : 2}]


@app.get("/")
def get():
    return {"message" : "This is message"}


@app.post("/posts")
def get_posts(post:Posts):
    print(type(post))
    data_dic = post.model_dump()
    data_dic["id"] = randrange(0,1000000)
    return {"data" : data_dic}


def find_id(id):
    for i in my_post_data:
        if i["id"] == id:
            return i
        

@app.post("/posts/{id}")
def getposts(id:int):
    data = find_id(id)
    return {"data" : data}