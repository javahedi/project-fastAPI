from telnetlib import NEW_ENVIRON
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from random import randrange
# run the Postgrs server
import psycopg2
# to return the Postgres table with their volumn title
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session
from . import models
from .database import  engine, get_db

#-----------------------------
models.Base.metadata.create_all(bind=engine)

#-----------------------------
app = FastAPI()

#-----------------------------
# pydantic --> input structure 
class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None


#-----------------------------
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

# test
@app.get("/tests")
def test_post(db: Session = Depends(get_db)):
    return {'status' : 'Succes'}


#-----------------------------
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def creat_posts(post : Post):
    cursor.execute(""" INSERT INTO posts (title, contnet, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, 
    post.content, post.published),)
    new_post = cursor.fetchone()
    conn.commit()
    return {'data' : new_post}

#-----------------------------
@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} not found")
    return {"post detail" : post}

#-----------------------------
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#-----------------------------
@app.put("/posts/{id}")
def update_post(id : int, post : Post):
    cursor.execute("""UPDATE posts SET title = %s, contnet = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)),)
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} does not exist!")
    return {'updated data' : updated_post}
