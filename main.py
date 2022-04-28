from enum import unique
from unicodedata import name
from fastapi import FastAPI, Depends, HTTPException


import sqlalchemy
from fastapi import FastAPI, Depends
from pydantic import BaseConfig, Field
from typing import Optional, List
from databases import Database


from pydantic import BaseModel, Field
from typing import Optional, List



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
    book_1: Optional[str] = None
    book_2: Optional[str] = None
    book_3: Optional[str] = None
    


DATABASE_URL = 'sqlite:///./library.db'


metadata = sqlalchemy.MetaData()

database = Database(DATABASE_URL)

books = sqlalchemy.Table(
    'books',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key = True),
    sqlalchemy.Column('name', sqlalchemy.String(50))
)
students = sqlalchemy.Table(
    'students',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key = True),
    sqlalchemy.Column('name', sqlalchemy.String(50))
)
inventory = sqlalchemy.Table(
    'inventory',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key = True),
    sqlalchemy.Column('book_id', sqlalchemy.Integer),
    sqlalchemy.Column('count_books',sqlalchemy.Integer),
    sqlalchemy.Column('borrow_count',sqlalchemy.Integer)
)

borrow = sqlalchemy.Table(
    'borrow',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key = True),
    sqlalchemy.Column('stu_id', sqlalchemy.Integer),
    sqlalchemy.Column('book_id', sqlalchemy.Integer)    
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args = {'check_same_thread':False})

metadata.create_all(engine)


app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def connect():
    await database.disconnect()

@app.get("/")
async def root():
    return {"api added": "goto /docs for api execution"}

@app.get("/books")
async def root():
    query = books.select()
    record = await database.fetch_all(query)
    return record

@app.get("/students")
async def root():
    query = students.select()
    record = await database.fetch_all(query)
    return record

@app.get("/viewinventory")
async def root():
    query = inventory.select()
    record = await database.fetch_all(query)
    return record

@app.get("/viewborrow")
async def root():
    query = borrow.select()
    record = await database.fetch_all(query)
    return record

@app.post("/addstudent")
async def add_student(student: Students):
    stu = students.insert().values(
        name = student.name
    )
    record = await database.execute(stu)
    query = students.select()
    record = await database.fetch_all(query)
    return record

@app.post("/addbook") 
async def add_book(book: Books):
    book = books.insert().values(
        name = book.book_name
    )
    record = await database.execute(book)
    query = books.select()
    record = await database.fetch_all(query)
    return record
    

@app.post("/addinventory")
async def update_inventory(store: Inventory):
    bk_id = store.book_id
    query = books.select()
    record = await database.fetch_all(query)
    dic = dict(record)
    #print(dic)
    if bk_id not in dic:
        raise HTTPException(status_code=404, detail="Book does not exist. Add book")
    query = inventory.select()
    record = await database.fetch_all(query)
    for i in record:
        if i[1] == bk_id:
            query = inventory.update().where(inventory.c.book_id == bk_id).values(count_books = store.count_books)
            record = await database.execute(query)
            raise HTTPException(status_code=200, detail = "Book already existed. Changed count of books")
    rde = inventory.insert().values(
        book_id = store.book_id,
        count_books = store.count_books,
        borrow_count = 0
    )
    record = await database.execute(rde)
    query = inventory.select()
    record = await database.fetch_all(query)
    return record

@app.post("/borrowbook")
async def update_inventory(std_id: int, book_name: str):
    query = students.select()
    record = await database.fetch_all(query)
    dic = dict(record)
    if std_id not in dic:
        raise HTTPException(status_code=404, detail="Student does not exist. Add new student")
    query = books.select()
    record = await database.fetch_all(query)
    dic = dict(record)
    book_id = -1
    for i in dic:
        if dic[i].lower() == book_name.lower():
            book_id = i
            break
    if book_id == -1:
        raise HTTPException(status_code=404, detail="Book does not exist. Add new Book")
    query = borrow.select().where(borrow.c.stu_id == std_id)
    record = await database.fetch_all(query)
    if len(record) == 3:
        raise HTTPException(status_code=402, detail="Student has already approached limit. Cannot borrow more books.")
    query = inventory.select().where(inventory.c.book_id == book_id)
    stmt = inventory.update().values(borrow_count = inventory.c.borrow_count + 1, count_books = inventory.c.count_books - 1 ).where(inventory.c.book_id == book_id)
    record = await database.execute(stmt)
    query = inventory.select().where(inventory.c.book_id == book_id)
    record = await database.fetch_one(query)
    print(record)
    if record[2] == 0:
        raise HTTPException(status_code=402, detail="Books not available.")    
    bw = borrow.insert().values(
        book_id = book_id,
        stu_id = std_id
    )
    record = await database.execute(bw) 
    return {'issue': 'Need to add this to borrow'}

@app.post("/returnbook")
async def update_inventory(std_id: int, book_name: str):
    query = students.select()
    record = await database.fetch_all(query)
    dic = dict(record)
    if std_id not in dic:
        raise HTTPException(status_code=404, detail="Student does not exist. Please check again")
    query = books.select()
    record = await database.fetch_all(query)
    dic = dict(record)
    book_id = -1
    for i in dic:
        if dic[i].lower() == book_name.lower():
            book_id = i
            break
    if book_id == -1:
        raise HTTPException(status_code=404, detail="Book does not exist. Please check again")
    query = borrow.select().where(borrow.c.stu_id == std_id)
    record = await database.fetch_all(query)
    flg = 1
    for i in record:
        if i[2] == book_id:
            flg = 0
    if flg == 1:
        raise HTTPException(status_code=404, detail="Student does not have the book. Please check again")
    stmt = inventory.update().values(count_books = inventory.c.count_books + 1 ).where(inventory.c.book_id == book_id)
    record = await database.execute(stmt)
    stmt = borrow.delete().where(borrow.c.stu_id == std_id, borrow.c.book_id == book_id)
    record = await database.execute(stmt)
    return {'issue': 'Need to add this to return'}