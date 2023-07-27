from pydantic import BaseModel, AnyUrl
from datetime import datetime


class UrlBase(BaseModel):
    original_url: AnyUrl 


class UrlCreate(UrlBase):
    ...


class Url_(UrlBase):
    shorten_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
