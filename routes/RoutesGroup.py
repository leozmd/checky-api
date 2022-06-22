from tokenize import group
from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelGroup import groups
from schemas.SchemaGroup import Group
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin
from middlewares.VerifyTokenRoute import VerifyTokenRoute

group = APIRouter(route_class=VerifyTokenRoute)


@group.get('/groups', status_code=200)
async def getAll(response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                return conn.execute(groups.select()).fetchall()
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@group.get('/groups/{idGrupo}', status_code=200)
async def getById(idGrupo: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(groups.select().where(
                    groups.c.idGrupo == idGrupo)).fetchone()
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


@group.post('/groups', status_code=201)
async def insert(grupo: Group, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(groups.select().where(
                    groups.c.tipoGrupo == grupo.tipoGrupo))
                if data is None:
                    conn.execute(groups.insert().values(
                        tipoGrupo=grupo.tipoGrupo
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


@group.put('/groups/{idGrupo}', status_code=204)
async def update(idGrupo: int, grupo: Group, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(groups.select().where(
                    groups.c.idGrupo == idGrupo)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    data = conn.execute(groups.select().where(
                        groups.c.tipoGrupo == grupo.tipoGrupo))
                    if data is None:
                        conn.execute(groups.update().values(
                            tipoGrupo=grupo.tipoGrupo
                        ).where(groups.c.idGrupo == idGrupo))
                    else:
                        response.status_code = status.HTTP_409_CONFLICT
            except SQLAlchemyError as e:
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@group.delete('/groups/{idGrupo}', status_code=204)
async def delete(idGrupo: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(groups.select().where(
                    groups.c.idGrupo == idGrupo)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    conn.execute(groups.delete().where(groups.c.idGrupo == idGrupo))
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
