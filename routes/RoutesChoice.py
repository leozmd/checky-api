from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelChoice import choices
from schemas.SchemaChoice import Choice
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin, isStudent
from middlewares.VerifyTokenRoute import VerifyTokenRoute

choice = APIRouter(route_class=VerifyTokenRoute)


@choice.get('/choices/{idPregunta}', status_code=200)
async def getByQuestionId(idPregunta: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        admin = isAdmin(role)
        if not admin:
            try:
                data = conn.execute("call PEleccionPregunta(?)", idPregunta).fetchone()
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


@choice.post('/choices', status_code=201)
async def insert(eleccion: Choice, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isStudent(role)
        if permission:
            try:
                data = conn.execute(choices.select().where(
                    choices.c.idRespuesta == eleccion.idRespuesta))
                if data is None:
                    conn.execute(choices.insert().values(
                        idRespuesta = eleccion.idRespuesta
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
