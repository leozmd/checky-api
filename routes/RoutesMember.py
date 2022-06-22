from fastapi import APIRouter, Header, Response, status
from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelMember import members
from schemas.SchemaMember import Member
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isMember, isTeacher, isAdmin
from middlewares.VerifyTokenRoute import VerifyTokenRoute


member = APIRouter(route_class=VerifyTokenRoute)


@member.get('/classrooms/{idClase}/members', status_code=200)
async def getByClassId(idClase: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        user = credentials['idUsuario']
        permission = isAdmin(role)
        permission1 = isTeacher(role)
        if permission | permission1:
            permission = isMember(user, idClase)
            if permission:
                try:
                    return conn.execute(members.select()).fetchall()
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


@member.get('/members/{idMiembro}', status_code=200)
async def getById(idMiembro: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        user = credentials['idUsuario']
        permission = isTeacher(role)
        if permission:
            try:
                data = conn.execute(members.select().where(
                    members.c.idMiembro == idMiembro)).fetchone()
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


@member.post('/members', status_code=201)
async def insert(miembro: Member, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(members.select().where(
                    members.c.idUsuario == miembro.idUsuario &
                    members.c.idClase == miembro.idClase))
                if data is None:
                    conn.execute(members.insert().values(
                        idUsuario = miembro.idUsuario,
                        idClase = miembro.idClase
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


@member.delete('/members/{idMiembro}', status_code=204)
async def delete(idMiembro: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(members.select().where(
                    members.c.idMiembro == idMiembro)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    conn.execute(members.delete().where(members.c.idMiembro == idMiembro))
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@member.get('/members/{idMiembro}/performance', status_code=200)
async def getPerformance(idClase: int, idMiembro: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        user = credentials["idUsuario"]
        role = credentials["idRol"]
        permission = isTeacher(role)
        if permission:
            permission = isMember(user, idClase)
            if permission:
                try:
                    correct_answers = conn.execute(
                        'call PRespuestasMiembro(?)', idMiembro).fetchone()
                    total_questions = conn.execute(
                        'call PPreguntasClase(?)', idClase).fetchone()
                    total_records = conn.execute(
                        'call PRegistrosMiembro(?)', idMiembro).fetchone()
                    class_lists = conn.execute('call PListasClase(?)', idClase).fetchone()
                    question_performance = int(
                        correct_answers[0]) / int(total_questions[0])
                    list_performance = int(total_records[0]) / int(class_lists[0])
                    total_performance = (
                        (question_performance + list_performance) / 2) * 100
                    return {
                        "Respuestas correctas": f"{correct_answers} en {total_questions} pregunta(s).",
                        "Asistencias": f"{total_records} en {class_lists} pase(s) de lista.",
                        "Desempeño total": f"{total_performance}%"
                    }
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