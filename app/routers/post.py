from .. import models , schema , utils ,oauth2
from fastapi import FastAPI , Response , status , HTTPException,Depends , APIRouter 
from sqlalchemy.orm import Session 
from sqlalchemy import func
from typing import List , Optional
from app.database import get_db 


router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)




# Get data--------------------------------------------

@router.get("/", response_model=List[schema.PostOut])
# @router.get("/")
def get_posts(db:Session = Depends(get_db),current_user : schema.UserOut = Depends(oauth2.get_current_user), limit : int = 10 , skip : int = 0 , search : Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(models.Post)
   
    result= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return result


# create data--------------------------------------------
@router.post("/",status_code=status.HTTP_201_CREATED , response_model=schema.Post)
def create_posts(post:schema.PostCreate, db:Session = Depends(get_db), current_user : schema.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title, post.content,post.published))
    # new_posts = cursor.fetchone()
    # conn.commit()
    

    # ownwer id is foragin key here 
    # we need to give foragin key while creating new post

    
    new_posts = models.Post(owner_id = current_user.id,**post.model_dump())

    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)

    return new_posts
    


# get data with id--------------------------------------------
@router.get("/{id}" , response_model=schema.PostOut)
def get_post(id : int, db:Session = Depends(get_db) , current_user : schema.UserOut = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()
    print(f"Getting post data {current_user.id}",)

    post = db.query(models.Post).filter(models.Post.id == id).first()


    result= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).all()


    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    
    return result



#delete data--------------------------------------------
   
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db) , current_user : schema.UserOut = Depends(oauth2.get_current_user)):
    # post request for delted
    # find the index in the array that hase required id 
    # my_post.pop(index)

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

   
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post with id : {id} dose not exist")
    
    if current_user.id != post.owner_id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorised to perform requested action")
    
    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update data--------------------------------------------
@router.put("/{id}" ,  response_model=schema.Post)
def update_post(id:int , updated_post:schema.PostCreate , db:Session = Depends(get_db) , current_user : schema.UserOut = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

   
  

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    
    if  post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} dose not exist")
    
    if  current_user.id != post.owner_id :

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not authorised to edit this post ")
    
    post_query.update(updated_post.model_dump(),synchronize_session=False) # type: ignore
    db.commit()

    return post


