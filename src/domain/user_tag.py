from pydantic import BaseModel

from src.domain.page_info import PageInfo
from src.domain.alcohol import AlcoholBasicInfo


class UserTag(BaseModel):
    tag_id: int
    tag_name: str

    class Config:
        orm_mode = True


class UserTagCreate(BaseModel):
    tag_name: str
    user_id: int
    alcohol_ids: list[int] = []


class PaginatedUserTag(BaseModel):
    user_tags: list[UserTag]
    page_info: PageInfo


class UserTagUpdateAlcohols(BaseModel):
    alcohol_ids: list[int] = []


class UserTagAlcohols(UserTag):
    alcohols: list[AlcoholBasicInfo] = []
