from pydoc import plain
from  passlib.context import CryptContext
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password : str):
    return pwd_content.hash(password)

def verify(plain_passwrod, hashed_password):
    return pwd_content.verify(plain_passwrod, hashed_password)