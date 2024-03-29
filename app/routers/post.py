from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user), 
                 limit: int = 15, skip: int= 0, search: Optional[str] = ""):
    #cursor.execute("""select * from posts """)
    #posts = cursor.fetchall()
 
   # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user) ):
    #print(post.dict())
    #return {"new_post" : f"title: {payload['title']} content: {payload['content']}"}
    #post_dict = post.model_dump()
    #post_dict['id']= randrange(0, 1000000)
    #my_post.append(post_dict)
    #cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   #(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #new_post = models.Post(title=post.title, content=post.content, published=post.published )

    new_post = models.Post(owner_id =current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
#def get_post(id: int, response: Response):
def get_post(id: int, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT *from posts where id = %s """,(str(id)))
    #test_post = cursor.fetchone()
    #test_post = db.query(models.Post).filter(models.Post.id == id).first()
    test_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(test_post)
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id:{id} was not found"}
    
    return test_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    #deleting post
    #find the index in the array that has required id 
    #my.posts.pop(index)

    #cursor.execute("""delete from posts where id = %s returning *""",(str(id),))
    #deleted_row = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data found for {id}")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized ")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""UPDATE posts set  title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   #(post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    updated_query = db.query(models.Post).filter(models.Post.id == id)
    post = updated_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data found for {id}")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized ")
    
    #post_dict = post.model_dump()
    #post_dict['id'] = id
    #my_post[index] = post_dict
    updated_query.update(update_post.model_dump(),synchronize_session=False)
    db.commit()
    return updated_query.first()

