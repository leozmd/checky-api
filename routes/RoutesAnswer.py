from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelAnswer import answers
from schemas.SchemaAnswer import Answer
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin, isTeacher
from middlewares.VerifyTokenRoute import VerifyTokenRoute

answer = APIRouter(route_class=VerifyTokenRoute)


@answer.get('/answers/{idPregunta}', status_code=200)
async def getByQuestionId(idPregunta: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        admin = isAdmin(role)
        if not admin:
            try:
                data = conn.execute(answers.select().where(
                    answers.c.idPregunta == idPregunta)).fetchall()
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


@answer.post('/answers', status_code=201)
async def insert(respuesta: Answer, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isTeacher(role)
        if permission:
            try:
                data = conn.execute(answers.select().where(
                    answers.c.txtRespuesta == respuesta.txtRespuesta & 
                    answers.c.edoRespuesta == respuesta.edoRespuesta &
                    answers.c.idPregunta == respuesta.idPregunta))
                if data is None:
                    conn.execute(answers.insert().values(
                        txtRespuesta = respuesta.txtRespuesta,
                        edoRespuesta = respuesta.edoRespuesta,
                        idPregunta = respuesta.idPregunta
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
