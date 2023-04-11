# VisitorsBook API with FastAPI and PostgreSQL

VisitorsBook api is a rest api build using FastAPI and postgreSQL. 
API has multiple endpoints
Endpoints: 
    - Register
    - Activate
    - Write a message
    - Update a Message
    - Read a Message
    - Read all Messages
    - delete a message 
    - Upvote a message
    - Viewing upvoted messages


A database using postgresql library psycopg2 is created to store the data. Database is created and stored on railway app. 

HTTP authentication system is  used before user can perform any operation. Users receive an authentication token on their emails to activate the account. 


![img](https://github.com/Siddharthbadal/VisitorsBook-API/blob/main/images/visitorbookapi.png)


