from typing import List, Optional

from pydantic import BaseModel


class BooksBase(BaseModel):
    book_name: str
    


class BooksCreate(BooksBase):
    pass


class Books(BooksBase):
    id: int
    book_name: str

    class Config:
        orm_mode = True


class StudentsBase(BaseModel):
    name: str
    


class StudentCreate(StudentsBase):
    pass


class Students(StudentsBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class Inventory(BaseModel):
    book_id: int
    count: int

class InventoryUpdate(Inventory):
    pass

class InventoryItem(Inventory):
    id: int
    book_id: int
    count: int

    class Config:
        orm_mode = True