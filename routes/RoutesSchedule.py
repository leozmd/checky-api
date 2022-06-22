from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelSchedule import schedules
from schemas.SchemaSchedule import Schedule
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin
from middlewares.VerifyTokenRoute import VerifyTokenRoute

schedule = APIRouter(route_class=VerifyTokenRoute)


@schedule.get('/schedules', status_code=200)
async def getAll(response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                return conn.execute(schedules.select()).fetchall()
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@schedule.get('/schedules/{idHorario}', status_code=200)
async def getById(idHorario: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(schedules.select().where(
                    schedules.c.idHorario == idHorario)).fetchone()
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


@schedule.post('/schedules', status_code=201)
async def insert(horario: Schedule, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(schedules.select().where(
                    schedules.c.diaHorario == horario.diaHorario &
                    schedules.c.iniHorario == horario.iniHorario &
                    schedules.c.finHorario == horario.finHorario))
                if data is None:
                    conn.execute(schedules.insert().values(
                        diaHorario = horario.diaHorario,
                        iniHorario = horario.iniHorario,
                        finHorario = horario.finHorario
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


@schedule.put('/schedules/{idHorario}', status_code=204)
async def update(idHorario: int, horario: Schedule, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(schedules.select().where(
                    schedules.c.idHorario == idHorario)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    data = conn.execute(schedules.select().where(
                        schedules.c.diaHorario == horario.diaHorario &
                        schedules.c.iniHorario == horario.iniHorario &
                        schedules.c.finHorario == horario.finHorario))
                    if data is None:
                        conn.execute(schedules.update().values(
                            diaHorario = horario.diaHorario,
                            iniHorario = horario.iniHorario,
                            finHorario = horario.finHorario
                        ).where(schedules.c.idHorario == idHorario))
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


@schedule.delete('/schedules/{idHorario}', status_code=204)
async def delete(idHorario: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(schedules.select().where(
                    schedules.c.idHorario == idHorario)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    conn.execute(schedules.delete().where(schedules.c.idHorario == idHorario))
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
