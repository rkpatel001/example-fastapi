from jose import JWTError , jwt
import secrets
from datetime import datetime , timedelta ,timezone
from . import schema , database , models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# Expriation time


SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encoded_jwt =jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    
    try : 
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schema.TokenData(id = id)
    except JWTError :
        raise credentials_exception
    

    return token_data

def get_current_user(token: str = Depends(oauth2_schema), db:Session  = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials" , headers={"WWW-Authenticate" : "Bearer"})

    token_data = verify_access_token(token,credentials_exception)
    print(token_data.id)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    
    if user is None:
        raise credentials_exception
    
    return user


        