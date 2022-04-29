from pydantic import BaseConfig, Field, BaseModel

class Books(BaseModel):
    id: int
    book_name: str = Field(...)

class Students(BaseModel):
    id: int
    name: str = Field(...)

class Inventory(BaseModel):
    id: int
    book_id: int
    count_books: int
    borrow_count: int

class Borrow(BaseModel):
    id: int
    stu_id : int
    book_id: int