from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelQuestion import questions
from schemas.SchemaQuestion import Question
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin, isTeacher, isStudent
from middlewares.VerifyTokenRoute import VerifyTokenRoute

question = APIRouter(route_class=VerifyTokenRoute)


@question.get('/questions/{idPregunta}', status_code=200)
async def getById(idPregunta: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        admin = isAdmin(role)
        if not admin:
            try:
                data = conn.execute(questions.select().where(
                    questions.c.idPregunta == idPregunta)).fetchone()
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


@question.get('/member/{idMiembro}/questions/', status_code=200)
async def getById(idMiembro: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isStudent(role)
        if permission:
            try:
                data = conn.execute(questions.select().where(
                    questions.c.idMiembro == idMiembro)).fetchone()
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


@question.post('/questions', status_code=201)
async def insert(pregunta: Question, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isTeacher(role)
        if permission:
            try:
                conn.execute(questions.insert().values(
                    txtPregunta = pregunta.txtPregunta,
                    idMiembro = pregunta.idMiembro
                ))
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
