
from pydantic import BaseModel

class ArticleBase(BaseModel):
    title: str
    context: str
    user_id: int 
    class Config:
        from_attributes=True


class ArticleID(ArticleBase):
    id: int


