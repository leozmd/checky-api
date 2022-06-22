from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelList import lists
from schemas.SchemaList import List
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin, isMember, isTeacher
from middlewares.VerifyTokenRoute import VerifyTokenRoute

list = APIRouter(route_class=VerifyTokenRoute)


@list.get('/classrooms/{idClase}/lists', status_code=200)
async def getByClassId(idClase: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        user = credentials['idUsuario']
        admin = isAdmin(role)
        if not admin:
            permission = isMember(user, idClase)
            if permission:
                try:
                    return conn.execute(lists.select().where(
                    lists.c.idClase == idClase)).fetchall()
                except SQLAlchemyError as e:
                    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                    return {
                        "msg": e
                    }
            else:
                response.status_code = status.HTTP_401_UNAUTHORIZED
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@list.get('/lists/{idLista}', status_code=200)
async def getById(idLista: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        user = credentials['idUsuario']
        admin = isAdmin(role)
        if not admin:
            try:
                data = conn.execute(lists.select().where(
                    lists.c.idLista == idLista)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    idClase = data[2]
                    permission = isMember(user, idClase)
                    if permission:
                        return data
                    else:
                        response.status_code = status.HTTP_401_UNAUTHORIZED
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@list.post('/lists', status_code=201)
async def insert(lista: List, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        user = credentials['idUsuario']
        permission = isTeacher(role)
        if permission:
            permission = isMember(user, lista.idClase)
            if permission:
                try:
                    data = conn.execute(lists.select().where(
                        lists.c.diaLista == lista.diaLista &
                        lists.c.idClase == lista.idClase))
                    if data is None:
                        conn.execute(lists.insert().values(
                            diaLista = lista.diaLista,
                            idClase = lista.idClase
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
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
