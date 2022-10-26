from turtle import title
from typing import Optional
from fastapi import Body, FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from random import randint, randrange

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating:Optional[int] = None


my_posts= [{"title":"post1 title","content":"post1 content","id":1},
{"title":"post2 title","content":"post2 content","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

# route or path operation
@app.get("/")
async def root():
    return {"message": "HEYYYY WELCOMEEE TO MY API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data":post_dict}
#  titlle: str ,content str


@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    post= find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found")
        
    return {"post_details": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index= find_index_post(id)

    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    print(post)
    index= find_index_post(id)

    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exist")
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict

    return {"m":post_dict}