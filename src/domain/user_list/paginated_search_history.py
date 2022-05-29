from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.user_list.search_history import SearchHistoryEntry


class PaginatedSearchHistory(BaseModel):
    alcohols: list[SearchHistoryEntry]
    page_info: PageInfo
