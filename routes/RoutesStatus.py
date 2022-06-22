from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelStatus import statuses
from schemas.SchemaStatus import Status
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin
from middlewares.VerifyTokenRoute import VerifyTokenRoute

status = APIRouter(route_class=VerifyTokenRoute)


@status.get('/statuses', status_code=200)
async def getAll(response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                return conn.execute(statuses.select()).fetchall()
            except SQLAlchemyError as e:

                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@status.get('/statuses/{idEstado}', status_code=200)
async def getById(idEstado: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(statuses.select().where(statuses.c.idEstado == idEstado)).fetchone()
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
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@status.post('/statuses', status_code= 201)
async def insert(estado: Status, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(statuses.select().where(statuses.c.tipoEstado ==
                                    estado.tipoEstado & statuses.c.resEstado == estado.resEstado)).fetchone()
                if data is None:
                    conn.execute(statuses.insert().values(
                        tipoEstado=estado.tipoEstado,
                        resEstado=estado.resEstado
                    ))
                else:
                    response.status_code = status.HTTP_409_CONFLICT
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED



@status.put('/statuses/{idEstado}', status_code=204)
async def update(idEstado: int, estado: Status, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(statuses.select().where(
                    statuses.c.idEstado == idEstado)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    data = conn.execute(statuses.statuses().where(
                        statuses.c.tipoEstado == estado.tipoEstado & statuses.c.resEstado == estado.resEstado)).fetchone()
                    if data is None:
                        conn.execute(statuses.update().values(
                            tipoEstado=estado.tipoEstado,
                            resEstado=estado.resEstado
                        ).where(statuses.c.idEstado == idEstado))
                    else:
                        response.status_code = status.HTTP_409_CONFLICT
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@status.delete('/statuses/{idEstado}', status_code=204)
async def delete(idEstado: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(statuses.select().where(
                    statuses.c.idEstado == idEstado)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    conn.execute(statuses.delete().where(
                        statuses.c.idEstado == idEstado))
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
