from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from random import randrange
# run the Postgrs server
import psycopg2
# to return the Postgres table with their volumn title
from psycopg2.extras import RealDictCursor 
import time

while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host = 'localhost', database='fastapi', 
                                    user ='postgres', password='Jimboo1155',
                                cursor_factory=RealDictCursor )

        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print('database connection was succesfull!!!')
        break
    except Exception as error:
        print('database connection was failed!!!')
        print('Erorr : ',  error)
        time.sleep(2)

        


#-----------------------------
app = FastAPI()

#-----------------------------
myPosts = [{"title":"post 1", "content" : "sth 1", "id" : 1},
           {"title":"post 2", "content" : "sth 2", "id" : 2},
           {"title":"post 3", "content" : "sth 3", "id" : 3}]
#-----------------------------
class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

#-----------------------------
def find_post(id):
    for p in myPosts:
        if p["id"]==id:
            return p

#-----------------------------
def find_index_post(id):
    for i,p in enumerate(myPosts):
        if p["id"]==id:
            return i

#-----------------------------
@app.get("/")
def root():
    return {"message" : "Hello world!"}

#-----------------------------
@app.get("/posts")
def get_posts():
    # Execute a query
    cursor.execute(""" SELECT * FROM posts""")
    # Retrieve query results
    posts = cursor.fetchall()
    return {"all posts" : posts}

#-----------------------------
@app.post("/posts", status_code=status.HTTP_201_CREATED)
#def creat_posts(post : dict=Body(...)):
def creat_posts(post : Post):
    post_dic = post.dict()
    post_dic['id'] = randrange(0,10000000)
    myPosts.append(post_dic)
    return {'data' : post_dic}

#-----------------------------
@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} not found")
    return {"post detai" : post}

#-----------------------------
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} not found")
    myPosts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#-----------------------------
@app.put("/posts/{id}")
def update_post(id : int, post : Post):
    index = find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} does not exist!")
    post_dic = post.dict()
    post_dic['id'] = id
    myPosts[index] = post_dic
    return {'data' : post_dic}
