from unicodedata import name
from fastapi import FastAPI, Depends, HTTPException
from numpy import std
import sqlalchemy
from schemas import Books, Students, Inventory, Borrow
from databases import Database
 
#connecting the database
DATABASE_URL = 'sqlite:///./library.db'

metadata = sqlalchemy.MetaData()
database = Database(DATABASE_URL)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata = sqlalchemy.MetaData()
metadata.reflect(bind=engine)
books = metadata.tables['books']

inventory = metadata.tables['inventory']
students = metadata.tables['students']
borrow = metadata.tables['borrow']

#fast api instance
app = FastAPI()
    

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def connect():
    await database.disconnect()

#endpoints
@app.get("/")
async def root():
    return {"api added": "goto /docs for api execution"}


@app.get("/books")
async def view_books():
    query = books.select()
    record = await database.fetch_all(query)
    return record

@app.get("/students")
async def view_students():
    query = students.select()
    record = await database.fetch_all(query)
    return record

@app.get("/viewinventory")
async def view_inventory():
    que = sqlalchemy.select(inventory.c.book_id, books.c.name, inventory.c.count_books, inventory.c.borrow_count).join(books)
    record = await database.fetch_all(que)
    return record

@app.get("/viewborrow")
async def view_borrow():
    query = borrow.select()
    que = sqlalchemy.select(borrow.c.id, books.c.name.label('Book name'), students.c.name.label('Student Name')).join(books, books.c.id == borrow.c.book_id).join(students, students.c.id == borrow.c.stu_id)
    record = await database.fetch_all(que)
    return record


@app.get("/top5")
async def view_top5():
    query = sqlalchemy.select(books.c.name, inventory.c.borrow_count).join(inventory, books.c.id == inventory.c.book_id).limit(5).order_by(sqlalchemy.desc(inventory.c.borrow_count))
    record = await database.fetch_all(query)
    return record    

@app.post("/addstudent")
async def add_student(student: Students):
    stu = students.insert().values(
        name = student.name
    )
    record = await database.execute(stu)
    return {'Detail':'New Student added successsfully'}

@app.post("/addbook") 
async def add_book(book: Books):
    book = books.insert().values(
        name = book.book_name
    )
    record = await database.execute(book)
    return {'Detail':'New Book added successsfully'}
    

@app.post("/addinventory")
async def add_update_inventory(store: Inventory):
    bk_id = store.book_id
    query = books.select().where(books.c.id == store.book_id)
    record = await database.fetch_all(query)
    #print(record)
    if record == []:
        raise HTTPException(status_code=404, detail="Book does not exist. Add book")
    query = inventory.select().where(inventory.c.book_id == store.book_id)
    record = await database.fetch_all(query)
    if record != []:
        query = inventory.update().where(inventory.c.book_id == bk_id).values(count_books = store.count_books)
        record = await database.execute(query)
        raise HTTPException(status_code=200, detail = "Book already existed. Changed count of books")           
    rde = inventory.insert().values(
        book_id = store.book_id,
        count_books = store.count_books,
        borrow_count = 0
    )
    record = await database.execute(rde)
    que = sqlalchemy.select(inventory.c.book_id, books.c.name, inventory.c.count_books, inventory.c.borrow_count).join(books)
    record = await database.fetch_all(que)
    return record

@app.post("/borrowbook")
async def update_borrow(std_id: int, book_name: str):   
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
    return {'Detail': 'Book borrowed successfuly'}

@app.post("/returnbook")
async def return_book(std_id: int, book_name: str):
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
    return {'Detail': 'Book returned successfuly'}

