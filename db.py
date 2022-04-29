import sqlalchemy
from databases import Database

#initializing the database
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
    sqlalchemy.Column('book_id', sqlalchemy.Integer, sqlalchemy.ForeignKey(books.c.id)),
    sqlalchemy.Column('count_books',sqlalchemy.Integer),
    sqlalchemy.Column('borrow_count',sqlalchemy.Integer)
)

borrow = sqlalchemy.Table(
    'borrow',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key = True),
    sqlalchemy.Column('stu_id', sqlalchemy.Integer, sqlalchemy.ForeignKey(students.c.id)),
    sqlalchemy.Column('book_id', sqlalchemy.Integer, sqlalchemy.ForeignKey(books.c.id))    
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args = {'check_same_thread':False})

metadata.create_all(engine)