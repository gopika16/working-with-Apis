from turtle import title
from fastapi import Body, FastAPI
from pydantic import BaseModel
app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    
# route or path operation
@app.get("/")
async def root():
    return {"message": "HEYYYY WELCOMEEE TO MY API"}

@app.get("/posts")
def get_posts():
    return {"data": "this is ur posts"}

@app.post("/createpost")
def create_posts(new_post:Post):
    print(new_post)
    return {"data":"new_post"}
#  titlle: str ,content str