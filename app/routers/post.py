from statistics import mode
from unittest import result
from app import oauth2, schemas
from .. import models ,schemas
from fastapi import Body, FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/",response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
limit:int = 3,skip:int = 0,search: Optional[str] ='' ):

 #for showing only owner posts
    # posts=db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    # when showing all posts
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    results = db.query(models.Post ,func.count(models.Vote.post_id).label("Votes")).join(models.Vote,models.Vote.post_id == models.Post.id,
    isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)

    # print(current_user.id)
    new_post=models.Post(owner_id= current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,
    # post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    return new_post
#  titlle: str ,content str


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post=cursor.fetchone()
    post=db.query(models.Post ,func.count(models.Vote.post_id).label("Votes")).join(models.Vote,models.Vote.post_id == models.Post.id,
    isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

# to get only the owners post
    # if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #    detail=f"Unauthorized Action")

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found")
        
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING * """,(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post_query =db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Unauthorized Action")
    
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,update_post:schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title =%s,content=%s,published=%s WHERE id=%s RETURNING * """,
    # (post.title,post.content,post.published,str(id)))

    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post =post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Unauthorized Action")
    
    post_query.update(update_post.dict(),synchronize_session=False)    
    db.commit()
    return post_query.first()