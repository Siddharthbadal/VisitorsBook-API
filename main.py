
from fastapi import FastAPI, Form
from routers import accounts, messages


app = FastAPI(title="VisitorsBook API",
              version="0.1.0",

              swagger_ui_parameters={"dafaultModelsExpandDepth": -1},
              contact={
                  "name":"Siddharth",
                  "url": "https://www.linkedin.com/in/siddharthbadal/",

              },
            description="""
                VisitorBook API - Leave your feedback here..
                
            """
              )

@app.get("/endpoints/")
async def read_about_endpoints():
    return [
        {
            "1": "Create Account",
            "2": "Write a message",
            "3": "Update a message",
            "4": "Delete a message",
            "5": "read all the messages",
            "6": "Upvote a message",
            "7": "View most upvoted messages",

        }
    ]

app.include_router(accounts.router)
app.include_router(messages.router)




























"""
@app.get("/hello")
def hello(db: Database = Depends(get_db)):
    db.cursor.execute("select * from track limit 2")
    data =db.cursor.fetchone()
    return {"message": "hello there", 'data': data}
"""









