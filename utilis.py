from passlib.context import CryptContext
from os import environ as env
import yagmail
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=['bcrypt'])

def get_password_hash(password):
    print(password)
    print(pwd_context.hash(password))
    print()
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def prep_and_send(email_to, activationurl):
    try:
        yag =yagmail.SMTP(env.get("GMAIL_ADDRESS") ,env.get("GMAIL_APP_PASSWORD"))
        subject = "VisitorBook API Account Activation"
        content = [
            f"Please click on the following link to activate your account.{activationurl}"
        ]
        yag.send(email_to, subject, content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unable to send email at this time. Please try again later! Your activation url is {activationurl}. Activate it now.  ")
