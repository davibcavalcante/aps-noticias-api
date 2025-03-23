from pydantic import BaseModel
from typing import List, Optional

class RSSItem(BaseModel):
    title: str
    link: str
    published: Optional[str]
    summary: Optional[str]
    image: Optional[str]

class RSSFeed(BaseModel):
    title: str
    link: str
    description: Optional[str]
    items: List[RSSItem]
