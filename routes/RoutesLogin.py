from fastapi import APIRouter, Response, status

from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from config.ConfigDB import conn
from models.ModelUser import users
from schemas.SchemaLogin import Login
from auth.JWTFunctions import writeToken


login = APIRouter()


@login.post('/login', status_code=200)
async def logIn(usuario: Login, response: Response):
    try:
        data = conn.execute(users.select().where(
            users.c.usuUsuario == usuario.usuUsuario)).fetchone()
        if data is None:
            response.status_code = status.HTTP_404_NOT_FOUND
        else:
            hashedpw = data[7].encode('utf-8')
            passUsuario = passUsuario.encode('utf-8')
            verif = bcrypt.checkpw(passUsuario, hashedpw)
            if verif == False:
                response.status_code = status.HTTP_400_BAD_REQUEST
            else:
                userdata = {
                    'idUsuario': data[0],
                    'idRol': data[8],
                    'idEstado': data[9]
                }
                token = writeToken(userdata)
                return {
                    "token": token
                }
    except SQLAlchemyError as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "msg": e
        }
