import jwt
from core.system_config import AUTH0
from fastapi import HTTPException, status
import datetime


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=AUTH0.ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, key=AUTH0.SECRET_KEY, algorithm=AUTH0.ALGORITHMS)

def decode_access_token(token: str) -> dict:
    try:
        encoded_jwt = jwt.decode(token, key=AUTH0.SECRET_KEY, algorithms=[AUTH0.ALGORITHMS], 
                                 audience=AUTH0.API_AUDIENCE, issuer=AUTH0.ISSUER)
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token")
    except jwt.exceptions.MissingRequiredClaimError:
        encoded_jwt = jwt.decode(token, key=AUTH0.SECRET_KEY, algorithms=[AUTH0.ALGORITHMS])
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Token has expired")
    return encoded_jwt