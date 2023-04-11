from fastapi import APIRouter, Form, Depends, HTTPException, status
from database import Database
from dependencies import get_db, validate_user

router = APIRouter(tags=['messages'])


@router.post("/messages" )
def write_a_message_on_the_visitorbook(message: str= Form(), private:bool=Form(False),
                                       db:Database = Depends(get_db),
                                       user_id: int = Depends(validate_user)
                                       ):


    message_id = db.write("visitorbook",['user_id','message', 'private'],[user_id, message, private])

    return {
        "message_id": message_id
    }





@router.get("/messages/most_upvoted_messages")
def get_most_upvoted_messages(db: Database= Depends(get_db)):
    messages = db.get("top_messages", ["id", "message", "upvotes"])
    print(messages)
    return messages


@router.patch("/messages/{message_id}")
def update_a_message(message_id: int, message: str= Form(...), private: bool = Form(False),
                        db: Database = Depends(get_db),
                        user_id: str = Depends(validate_user)):

    message_db = db.get_one("visitorbook", ['id', 'user_id'], where={'id': message_id})
    if not message_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Id not valid. Message not found!')
    # all msges getting updated with private value
    if message_db.get("user_id") == user_id:
        db.update("visitorbook", ["message", "private"], [message, private], where={"id":message_id})
        return {"status":"Message Updated!"}

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this message!")



@router.get("/messages/{message_id}")
def get_a_message(message_id: int, db: Database= Depends(get_db),
                  user_id: int = Depends(validate_user)):
    message= db.get_one(
        table='visitorbook',
        columns=['id', 'user_id', 'message', 'private', 'created_at'],
        where={'id': message_id}
    )
    if (not message) or (message['private'] and message['user_id'] != user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Message by given id not found or It is not your message! ')
    exclude = ['user_id', 'private']

    return {k: v for k, v in message.items() if k not in exclude}



@router.get("/messages")
def get_all_messages(num: int = 10, db: Database = Depends(get_db), user_id: str = Depends(validate_user)):
    messages = db.get(table='visitorbook', columns=['id','message','created_at'], where={'private':False}, or_where={"private":True, "user_id":user_id}, limit=num)

    return messages

    public_messages = db.get("visitorbook", ['id', "message", "created_at"], where={"private":False})
    private_messages = db.get("visitorbook", ['id', "message", "created_at"], where={'private': True, "user_id":user_id})
    # user id not working

    messages = public_messages + private_messages
    return messages[:num]



@router.delete("/messages/{message_id")
def delete_a_message(message_id: int, db:Database = Depends(get_db), user_id: str=Depends(validate_user)):
    message = db.get_one("visitorbook", ['id', 'user_id'], where={'id':message_id})
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found!")


    if message.get("user_id") == user_id:
        db.delete("visitorbook", where={'id': message_id})
        return {'status': "Message deleted!"}

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This is not your message. You can't delete it")


#
# @router.get("/messages/search")
# def search_for_messages_by_keyword(search_term: str, num:int=10, db:Database = Depends(get_db), user_id: int = Depends(validate_user)):
#     # messages = db.get("visitorbook",
#     #             ['id', 'message', 'private'],
#     #            where={'private': False},
#     #            or_where ={"private": True, "user_id": user_id},
#     #            contains={'message': search_term},
#     #                      limit=num)
#     public_msgs=db.get("visitorbook", ['id', 'message', 'private'], where={'private':False}, contains={'message':search_term})
#     private_msgs = [db.get("visitorbook", ['id', 'message', 'private'], where={'private':True, "user_id":user_id}, contains={'message':search_term})]
#
#     messages =public_msgs + private_msgs
#     return messages


@router.get("/messages/{message_id}/upvote")
def upvote_a_message(message_id: int, db:Database=Depends(get_db), user_id: str = Depends(validate_user)):
    message = db.get_one("visitorbook", ["id", "user_id", "private"], where={"id": message_id})

    if (not message) or (message['private'] and message['user_id'] != user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message is either private or does not exists in the visitor book!")

    if message["user_id"] == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can not upvote your own messages!")

    upvote = db.get_one("upvotes", ["id"], where={"user_id":user_id, "message_id":message_id})

    if upvote:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have already upvoted this message!")

    db.write("upvotes", ['user_id', "message_id"], [user_id, message_id])
    return {"status": f" You successfully upvoted message {str(message_id)}. Thank You!"}














