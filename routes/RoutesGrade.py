from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelGrade import grades
from schemas.SchemaGrade import Grade
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin
from middlewares.VerifyTokenRoute import VerifyTokenRoute

grade = APIRouter(route_class=VerifyTokenRoute)


@grade.get('/grades', status_code=200)
async def getAll(response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                return conn.execute(grades.select()).fetchall()
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@grade.get('/grades/{idGrado}', status_code=200)
async def getById(idGrado: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(grades.select().where(
                    grades.c.idGrado == idGrado)).fetchone()
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


@grade.post('/grades', status_code=201)
async def insert(grado: Grade, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(grades.select().where(
                    grades.c.tipoGrado == grado.tipoGrado))
                if data is None:
                    conn.execute(grades.insert().values(
                        tipoGrado=grado.tipoGrado
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


@grade.put('/grades/{idGrado}', status_code=204)
async def update(idGrado: int, grado: Grade, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(grades.select().where(
                    grades.c.idGrado == idGrado)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    data = conn.execute(grades.select().where(
                        grades.c.tipoGrado == grado.tipoGrado))
                    if data is None:
                        conn.execute(grades.update().values(
                            tipoGrado=grado.tipoGrado
                        ).where(grades.c.idGrado == idGrado))
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


@grade.delete('/grades/{idGrado}', status_code=204)
async def delete(idGrado: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(grades.select().where(
                    grades.c.idGrado == idGrado)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    conn.execute(grades.delete().where(grades.c.idGrado == idGrado))
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
