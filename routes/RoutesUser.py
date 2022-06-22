from fastapi import APIRouter, Header, Response, status
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from config.ConfigDB import conn
from models.ModelUser import users
from schemas.SchemaUser import User
from auth.JWTFunctions import validateToken
from auth.CredentialsFunctions import isAdmin
from middlewares.VerifyTokenRoute import VerifyTokenRoute


user = APIRouter(route_class=VerifyTokenRoute)


@user.get('/users', status_code=200)
async def getAll(response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials['idRol']
        permission = isAdmin(role)
        if permission:
            try:
                return conn.execute(users.select()).fetchall()
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@user.get('/users/profile', status_code=200)
async def getProfile(response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        idUsuario = credentials['idUsuario']
        try:
            data = conn.execute(users.select().where(
                users.c.idUsuario == idUsuario)).fetchone()
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


@user.post('/users', status_code=201)
async def insert(usuario: User, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials["idRol"]
        permission = isAdmin(role)
        if permission:
            passwd = usuario.passUsuario
            passwd = passwd.encode('utf-8')
            salt = bcrypt.gensalt()
            hashedpw = bcrypt.hashpw(passwd, salt)
            try:
                data = conn.execute(users.select().where(
                    users.c.usuUsuario == usuario.usuUsuario)).fetchone()
                if data is None:
                    data = conn.execute(users.select().where(
                        users.c.matUsuario == usuario.matUsuario)).fetchone()
                    if data is None:
                        conn.execute(users.insert().values(
                            nomUsuario=usuario.nomUsuario,
                            appatUsuario=usuario.appatUsuario,
                            apmatUsuario=usuario.apmatUsuario,
                            sexoUsuario=usuario.sexoUsuario,
                            matUsuario=usuario.matUsuario,
                            usuUsuario=usuario.usuUsuario,
                            passUsuario=hashedpw,
                            idRol=usuario.idRol,
                            idEstado=usuario.idEstado
                        ))
                    else:
                        response.status_code = status.HTTP_409_CONFLICT
                        return {
                            "msg": "Matricula ya existe"
                        }
                else:
                    response.status_code = status.HTTP_409_CONFLICT
                    return {
                        "msg": "Nombre de usuario ya existe"
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


@user.put('/users/{idUsuario}', status_code=204)
async def update(idUsuario: int, usuario: User, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials["idRol"]
        permission = isAdmin(role)
        if permission:
            passwd = usuario.passUsuario
            passwd = passwd.encode('utf-8')
            salt = bcrypt.gensalt()
            hashedpw = bcrypt.hashpw(passwd, salt)
            try:
                data = conn.execute(users.select().where(
                    users.c.idUsuario == idUsuario)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    data = conn.execute(users.select().where(users.c.nomUsuario == usuario.nomUsuario & users.c.appatUsuario == usuario.appatUsuario & users.c.apmatUsuario == usuario.apmatUsuario & users.c.sexoUsuario == usuario.sexoUsuario &
                                        users.c.matUsuario == usuario.matUsuario & users.c.usuUsuario == usuario.usuUsuario & users.c.passUsuario == hashedpw & users.c.idRol == usuario.idRol & users.c.idEstado == usuario.idEstado)).fetchone()
                    if data is None:
                        data = conn.execute(users.select().where(
                            users.c.usuUsuario == usuario.usuUsuario)).fetchone()
                        if data is None:
                            data = conn.execute(users.select().where(
                                users.c.matUsuario == usuario.matUsuario)).fetchone()
                            if data is None:
                                conn.execute(users.update().values(
                                    nomUsuario=usuario.nomUsuario,
                                    appatUsuario=usuario.appatUsuario,
                                    apmatUsuario=usuario.apmatUsuario,
                                    sexoUsuario=usuario.sexoUsuario,
                                    matUsuario=usuario.matUsuario,
                                    usuUsuario=usuario.usuUsuario,
                                    passUsuario=hashedpw,
                                    idRol=usuario.idRol,
                                    idEstado=usuario.idEstado
                                ).where(users.c.idUsuario == idUsuario))
                                
                            else:
                                response.status_code = status.HTTP_409_CONFLICT
                                return {
                                    "msg": "Matricula ya existe"
                                }
                        else:
                            response.status_code = status.HTTP_409_CONFLICT
                            return {
                                "msg": "Nombre de usuario ya existe"
                            }
                    else:
                        response.status_code = status.HTTP_409_CONFLICT
                        return {
                            "msg": "Ya existe un objeto con las características proporcionadas"
                        }
            except SQLAlchemyError as e:
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@user.delete('/users/{idUsuario}', status_code=204)
async def delete(idUsuario: int, response: Response, token: str = Header(None)):
    credentials = validateToken(token, output=True)
    if credentials != 401:
        role = credentials["idRol"]
        permission = isAdmin(role)
        if permission:
            try:
                data = conn.execute(users.select().where(
                    users.c.idUsuario == idUsuario)).fetchone()
                if data is None:
                    response.status_code = status.HTTP_404_NOT_FOUND
                else:
                    conn.execute(users.delete().where(
                        users.c.idUsuario == idUsuario))
            except SQLAlchemyError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "msg": e
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED