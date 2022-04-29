# FastApi_Library_Management

### - Objective
Design and create backend of a small application of school library management system.

### - How to run this app
First download this repo in your system. Make sure you have required libraries specified in requirements. Open the terminal and enter:<br>
> `python db.py`<br>
> `python schemas.py`<br>
> `uvicorn main:app --reload`<br>
> Copy `localhost:8000/docs` to see the APIs<br>

*There are 4 GET endpoints for retrieving information on books, students, inventory and borrow<br>
There are 5 POST endpoints for updating data into books, students, borrowing and returning of books<br>
There is 1 endpoint to list out the top 5 popular books based on no of ties the book is borrowed*

### - Table Structure
1. Books:
   | Field         | Data Type               | 
   | ------------- |:-----------------------:| 
   |  ID           | Integer and Primary Key | 
   | Book Name     | String                  |  
   
2. Students:
   | Field         | Data Type               | 
   | ------------- |:-----------------------:| 
   |  ID           | Integer and Primary Key | 
   |  Name         | String                  |  
  
3. Inventory:
   | Field         | Data Type                          | 
   | ------------- |:----------------------------------:| 
   |  ID           | Integer and Primary Key            | 
   |  Book_ID      | Integer and Foreign Key(Books - ID)| 
   |  Count_Books           | Integer             |
   |  Borrow_Count           | Integer             |
   
4. Borrow:
   | Field         | Data Type                          | 
   | ------------- |:----------------------------------:| 
   |  ID           | Integer and Primary Key            | 
   |  Stu_ID      | Integer and Foreign Key(Students - ID)| 
   |  BookID           | Integer             |
   
   
### - File Structure
   `db.py` file has statements that is responsible for creation of database<br>
   `schemas.py` file has statements that has structure of each table as a class<br>
   `main.py` file has all the end points  <br>
   
### - Output of the application in load - _localhost:8000/docs_   
 
   ![image](https://user-images.githubusercontent.com/55554547/165997244-e85c18cc-e96f-44ab-9269-87fc71c6e848.png)


