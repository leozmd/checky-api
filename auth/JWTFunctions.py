from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv


def expireDate(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date


def writeToken(data: dict):
    token = encode(
        payload={
            **data,
            "exp": expireDate(1)
        },
        key=getenv('SECRET'),
        algorithm="HS256"
    )
    return token


def validateToken(token, output=False):
    try:
        decodedToken = decode(
            token,
            key=getenv('SECRET'),
            algorithms=['HS256']
        )
        if output:
            return decodedToken
    except exceptions.DecodeError:

        return 401
    except exceptions.ExpiredSignatureError:

        return 401
