from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelRole import roles
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin
from middlewares.VerifyTokenRoute import VerifyTokenRoute

role = APIRouter(route_class=VerifyTokenRoute)


@role.get('/roles', status_code=200)
async def getAll(response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                return conn.execute(roles.select()).fetchall()
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@role.get('/roles/{idRol}')
async def getById(idRol: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        try:
            data = conn.execute(roles.select().where(roles.c.idRol == idRol)).fetchone()
            if data is None:
                response.status_code = status.HTTP_404_NOT_FOUND
            else:
                return data
        except SQLAlchemyError as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "msg": e
            }
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
