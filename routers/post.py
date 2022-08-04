
from pyexpat import model
from statistics import mode
from unittest import result
from fastapi import  HTTPException,  Response, status, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, oauth2, schemas
from app.database import  get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#-----------------------------
#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])  # after joinign 
def get_posts(db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user),
             limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # returning all posts, not matter which user requests
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # if you want to return post only related to current user
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    #return posts


    '''
    SQL version ;D

    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()

    posts = db.execute(
        'SELECT posts.*, COUNT( votes.post_id) SET AS votes FROM posts LEFY JOIN votes ON 
         post.id = votes.post_id GROUP BY  posts.id'
    )

    results = []
    for post on posts:
        results.append(dict(post))
    '''

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(posts)
    
    return posts


#-----------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def creat_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#-----------------------------
#@router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,  db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
   
   #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Not authorized to perform reqiested action.')

    return post


#-----------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,   db: Session = Depends(get_db), 
               current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Not authorized to perform reqiested action.')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#-----------------------------
@router.put("/{id}", response_model=schemas.Post)
def update_post(id : int, updated_post : schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
   
    post_querry = db.query(models.Post).filter(models.Post.id == id)
    post = post_querry.first()

    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} does not exist!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Not authorized to perform reqiested action.')


    post_querry.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_querry.first()
