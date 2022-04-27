# FastApi_Library_Management

### How to run this app
First download this repo in your system. Make sure you have required libraries specified in requirements. Open the terminal and enter:
`uvicorn main:app --reload`

### Table Structure
1. Books:
   ID - Integer and Primary Key
   Book Name - String
2. Students:
   ID - Integer and Primary Key
   Name - String
3. Inventory:
   ID - Integer and Primary Key
   Book_ID - Integer and Foreign Key(Books - ID)
   Count_Books - Integer
   Borrow_Count - Integer
4. Borrow:
   ID - Integer and Primary Key
   StuID - Integer and Foreign Key(Students - ID)
   BookID1 - Integer
   BookID1 - Integer
   BookID1 - Integer
   
