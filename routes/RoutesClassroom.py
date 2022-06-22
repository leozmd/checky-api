from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelClassroom import classrooms
from schemas.SchemaClassroom import Classroom
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin
from middlewares.VerifyTokenRoute import VerifyTokenRoute

classroom = APIRouter(route_class=VerifyTokenRoute)


@classroom.get('/classrooms', status_code=200)
async def getAll(response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                return conn.execute("SELECT * FROM VDatosClases").fetchall()
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@classroom.get('/classrooms/{idClase}', status_code=200)
async def getById(idClase: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute("call PDatosClase(?)", idClase).fetchone()
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


@classroom.post('/classrooms', status_code=201)
async def insert(clase: Classroom, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(classrooms.select().where(
                    classrooms.c.idCarrera == clase.idCarrera &
                    classrooms.c.idGrado == clase.idGrado &
                    classrooms.c.idTurno == clase.idTurno &
                    classrooms.c.idGrupo == clase.idGrupo &
                    classrooms.c.idAsignatura == clase.idAsignatura)).fetchone()
                if data is None:
                    conn.execute(classrooms.insert().values(
                        idCarrera = clase.idCarrera,
                        idGrado = clase.idGrado,
                        idTurno = clase.idTurno,
                        idGrupo = clase.idGrupo,
                        idAsignatura = clase.idAsignatura
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


@classroom.put('/classrooms/{idClase}', status_code=204)
async def update(idClase: int, clase: Classroom, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(classrooms.select().where(
                    classrooms.c.idClase == idClase)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    data = conn.execute(classrooms.select().where(
                    classrooms.c.idCarrera == clase.idCarrera &
                    classrooms.c.idGrado == clase.idGrado &
                    classrooms.c.idTurno == clase.idTurno &
                    classrooms.c.idGrupo == clase.idGrupo &
                    classrooms.c.idAsignatura == clase.idAsignatura))
                    if data is None:
                        conn.execute(classrooms.update().values(
                            idCarrera = clase.idCarrera,
                            idGrado = clase.idGrado,
                            idTurno = clase.idTurno,
                            idGrupo = clase.idGrupo,
                            idAsignatura = clase.idAsignatura
                        ).where(classrooms.c.idClase == idClase))
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


@classroom.delete('/classrooms/{idClase}', status_code=204)
async def delete(idClase: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(classrooms.select().where(
                    classrooms.c.idClase == idClase)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    conn.execute(classrooms.delete().where(classrooms.c.idClase == idClase))
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
