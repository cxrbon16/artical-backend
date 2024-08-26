from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, Sequence, UUID
from database import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime


class BaseModel(Base):
    __abstract__ = True ## allowing other tables to inherit from this class.
    __allow_unampped__ = True ## allowing applying unmapped method (?).
    id = Column(Integer, primary_key=True)

    

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    context = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    user_id = Column(ForeignKey("users.id"))
    # tags = relationship("Tag", secondary="article_tag_rel")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    tag_name = Column(String, index=True)
    tag_short = Column(String)
    # articles = relationship("Article", secondary="article_tag_rel")


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, index = True)
    number_of_post = Column(Integer) 
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    articles = relationship(Article)

Base.metadata.create_all(engine)
