from pydantic import BaseModel

class PaginationMetaSchema(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    limit: int