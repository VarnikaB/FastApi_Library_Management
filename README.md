# FastApi_Library_Management

### How to run this app
First download this repo in your system. Make sure you have required libraries specified in requirements. Open the terminal and enter:
`uvicorn main:app --reload`

### Table Structure
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
   |  BookID1           | Integer             |
   |  BookID2           | Integer             |
   |  BookID3           | Integer             |
   
   
