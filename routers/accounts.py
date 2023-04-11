from uuid import uuid4
from fastapi import FastAPI, APIRouter,Depends, Query, HTTPException, status, Form, Request
from database import Database
from dependencies import get_db
from pydantic import BaseModel, EmailStr, ValidationError, SecretStr
from utilis import get_password_hash, verify_password, prep_and_send
from psycopg2.errors import UniqueViolation


router = APIRouter(tags=['accounts'])


class User(BaseModel):
    email: EmailStr
    # EmailStr is a email validator in pydantic
    password: SecretStr
    # SecretStr is used to convert text into invisible format


@router.get("/activate" )
def activate(token: str, db:Database = Depends(get_db)):
    # search for token in database
    token = db.get_one("tokens", ['token','user_id'], where={'token': token})
    if token:

        is_account_active = db.get_one('users', ['active'], where={'id': token.get('user_id')})

        if is_account_active['active']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Account already actiavted!'
            )

        db.update('users', ['active', 'activated_at'], ['true', 'now()'], where= {'id': token.get('user_id')})
        return {'status': "Account activated."}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token!")





@router.post("/register", status_code=status.HTTP_201_CREATED)
# depends is to create dependency injection on other part code
def user_register( email: str, password: SecretStr = Query(default=None, min_length=8),
                  db:Database=Depends(get_db), req: Request = None):
    try:
        user = User(email=email, password=password)
        # get_secret_value() shows us back value in text
        token= str(uuid4())
        hashed_password = get_password_hash(password.get_secret_value())

        # with db.conn:
        #     db.cursor.execute(" INSERT INTO users (email, password) VALUES ( %s, %s)",
        #      (user.email, hashed_password))

        user_id=db.write('users', ['email','password'], [email, hashed_password])   # emails comes from query parameter
        db.write('tokens', ['token', 'user_id'], [token, user_id])

        activationurl = f"{req.base_url}activate?token={token}"
        prep_and_send(email, activationurl)


        return {"status": "Registration done. Please activate your account by clicking on the link send to your email.","user_id": user_id}
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email")
        return {"error": "This is Not a valid email!"}
    except UniqueViolation:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email already registered!")




@router.get("/all_users_here")
def get_all_users():
    pass