from fastapi import APIRouter, Header, Response, status

from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelRecord import records
from models.ModelList import lists
from models.ModelMember import members
from schemas.SchemaRecord import Record
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isTeacher, isMember, isStudent
from middlewares.VerifyTokenRoute import VerifyTokenRoute
from datetime import datetime, date

record = APIRouter(route_class=VerifyTokenRoute)



@record.get('/lists/{idLista}/records', status_code=200)
async def getByListId(idLista: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        user = credentials['idUsuario']
        permission = isTeacher(role)
        if permission:
            try:
                data = conn.execute(lists.select().where(
                    lists.c.idLista == idLista)).fetchone()
                idClase = data[2]
                permission = isMember(user, idClase)
                if permission:
                    data = conn.execute(records.select().where(
                        records.c.idLista == idLista)).fetchone()
                    if data is None:
                        response.status_code = status.HTTP_404_NOT_FOUND
                    else:
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


@record.get('/lists/{idLista}/records/members/{idMiembro}', status_code=200)
async def getByListAndMemberId(idLista: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        user = credentials['idUsuario']
        permission = isStudent(role)
        if permission:
            try:
                data = conn.execute(lists.select().where(
                    lists.c.idLista == idLista)).fetchone()
                idClase = data[2]
                permission = isMember(user, idClase)
                if permission:
                    member_data = conn.execute(members.select().where(members.c.idUsuario == user &
                    members.c.idClase == idClase))
                    idMiembro = member_data[0]
                    data = conn.execute(records.select().where(
                        records.c.idMiembro == idMiembro & records.c.idLista == idLista)).fetchone()
                    if data is None:
                        response.status_code = status.HTTP_404_NOT_FOUND
                    else:
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


@record.post('/records', status_code=201)
async def insert(registro: Record, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        user = credentials['idUsuario']
        permission = isStudent(role)
        if permission:
            try:
                data = conn.execute(lists.select().where(
                    lists.c.idLista == registro.idLista)).fetchone()
                idClase = data[2]
                permission = isMember(user, idClase)
                if permission:
                    data = conn.execute(records.select().where(
                        records.c.idMiembro == registro.idMiembro &
                        records.c.idLista == registro.idLista)).fetchone()
                    if data is None:
                        list_data = conn.execute(lists.select().where(
                            lists.c.idLista == registro.idLista
                        )).fetchone()
                        date_string = str(list_data[1])
                        list_date = datetime.strptime(date_string, '%Y-%m-%d').date()
                        if registro.diaRegistro == list_date:
                            conn.execute(records.insert().values(
                                diaRegistro = registro.diaRegistro,
                                horaRegistro = registro.horaRegistro,
                                idMiembro = registro.idMiembro,
                                idLista = registro.idLista
                            ))
                        else:
                            response.status_code = status.HTTP_400_BAD_REQUEST
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
