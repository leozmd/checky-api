from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelScheduleClassroom import classroom_schedules
from schemas.SchemaScheduleClassroom import ScheduleClassroom
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin, isMember
from middlewares.VerifyTokenRoute import VerifyTokenRoute

schedule_classroom = APIRouter(route_class=VerifyTokenRoute)


@schedule_classroom.get('/schedules/classroom/{idClase}', status_code=200)
async def getByClassId(idClase: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        user = credentials['idUsuario']
        permission = isAdmin(role)
        permission1 = isMember(user, idClase)
        if permission | permission1:
            try:
                data = conn.execute(classroom_schedules.select().where(
                    classroom_schedules.c.idClase == idClase)).fetchone()
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


@schedule_classroom.post('/schedules/classroom', status_code=201)
async def insert(horario: ScheduleClassroom, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(classroom_schedules.select().where(
                    classroom_schedules.c.idHorario == horario.idHorario &
                    classroom_schedules.c.idClase == horario.idClase))
                if data is None:
                    conn.execute(classroom_schedules.insert().values(
                        idHorario = horario.idHorario,
                        idClase = horario.idClase
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


@schedule_classroom.delete('/schedules/{idHorarioClase}', status_code=204)
async def delete(idHorarioClase: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(classroom_schedules.select().where(
                    classroom_schedules.c.idHorarioClase == idHorarioClase)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    conn.execute(classroom_schedules.delete().where(classroom_schedules.c.idHorarioClase == idHorarioClase))
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
