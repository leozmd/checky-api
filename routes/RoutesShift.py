from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelShift import shifts
from schemas.SchemaShift import Shift
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin
from middlewares.VerifyTokenRoute import VerifyTokenRoute

shift = APIRouter(route_class=VerifyTokenRoute)


@shift.get('/shifts', status_code=200)
async def getAll(response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                return conn.execute(shifts.select()).fetchall()
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@shift.get('/shifts/{idTurno}', status_code=200)
async def getById(idTurno: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(shifts.select().where(
                    shifts.c.idTurno == idTurno)).fetchone()
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


@shift.post('/shifts', status_code=201)
async def insert(turno: Shift, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(shifts.select().where(
                    shifts.c.nomTurno == turno.nomTurno)).fetchone()
                if data is None:
                    conn.execute(shifts.insert().values(
                        nomTurno=turno.nomTurno
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


@shift.put('/shifts/{idTurno}', status_code=204)
async def update(idTurno: int, turno: Shift, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(shifts.select().where(
                    shifts.c.idTurno == idTurno)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    data = conn.execute(shifts.select().where(
                        shifts.c.nomTurno == turno.nomTurno)).fetchone()
                    if data is None:
                        conn.execute(shifts.update().values(
                            nomTurno=turno.nomTurno
                        ).where(shifts.c.idTurno == idTurno))
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


@shift.delete('/shifts/{idTurno}', status_code=204)
async def delete(idTurno: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(shifts.select().where(
                    shifts.c.idTurno == idTurno)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    conn.execute(shifts.delete().where(shifts.c.idTurno == idTurno))
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
