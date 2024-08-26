from fastapi import FastAPI, Depends
from typing import Annotated
from pydantic import BaseModel, EmailStr
from databases import Database
from sqlalchemy import create_engine, MetaData
import models 
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from schemas.Article import ArticleID, ArticleBase


app = FastAPI()

class UserBase(BaseModel):
    '''
        User pydanctic model withOUT password.
    '''
    username: str
    email: EmailStr | None = None

class UserIn(UserBase):
    '''
        User pydanctic model with password.
    '''
    password: str
    class Config:
        from_attributes=True
class UserOut(UserBase):
    id: int



def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dep = Annotated[Session, Depends(get_db)]


@app.post("/users/")
async def create_user(user: UserIn, db: db_dep):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[UserBase])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User)
    return users


@app.post("/articles/")
async def create_post(article: ArticleBase, db: db_dep):
    db_article = models.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@app.get("/articles/")
async def get_all_posts(db: db_dep):
    result = db.query(models.Article).all()
    return result


@app.get("/users/{user_id}/articles")
async def get_users_articles(user_id: int, db: db_dep):
    articles_db = db.query(models.Article).filter(models.Article.user_id == user_id).all()
    return [ArticleBase.from_orm(article) for article in articles_db]


@app.get("/users/{user_id}", response_model=UserBase)
async def get_user(user_id: int, db: db_dep, ):
    user_db = db.query(models.User).filter(models.User.id == user_id).first()
    if user_db == None:
        return 
    res_user = UserIn.from_orm(user_db)
    return res_user 
