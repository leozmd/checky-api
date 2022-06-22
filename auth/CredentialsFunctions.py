from sqlalchemy.exc import SQLAlchemyError
from config.ConfigDB import conn
from models.ModelRole import roles
from models.ModelStatus import statuses
from models.ModelMember import members


def isEnrolled(idEstado: int):
    try:
        data = conn.execute(statuses.select().where(
            statuses.c.idEstado == idEstado))
        permission = data[2]
        if permission == 0:
            return True
        else:
            return False
    except SQLAlchemyError:
        return "Error al conectar a la base de datos"


def isAdmin(idRol: int):
    try:
        data = conn.execute(roles.select().where(roles.c.idEstado == idRol))
        role = data[1]
        if role == "Administrador":
            return True
        else:
            return False
    except SQLAlchemyError:
        return "Error al conectar a la base de datos"


def isTeacher(idRol: int, idEstado: int):
    enroll = isEnrolled(idEstado)
    if enroll:
        try:
            data = conn.execute(roles.select().where(
                roles.c.idEstado == idRol))
            role = data[1]
            if role == "Docente":
                return True
            else:
                return False
        except SQLAlchemyError:
            return "Error al conectar a la base de datos"
    else:
        return False


def isStudent(idRol: int, idEstado: int):
    enroll = isEnrolled(idEstado)
    if enroll:
        try:
            data = conn.execute(roles.select().where(
                roles.c.idEstado == idRol))
            role = data[1]
            if role == "Estudiante":
                return True
            else:
                return False
        except SQLAlchemyError:
            return "Error al conectar a la base de datos"
    else:
        return False


def isMember(idUsuario: int, idClase: int):
    try:
        data = conn.execute(members.select().where(
            members.c.idUsuario == idUsuario & members.c.idClase == idClase)).fetchone()
        if data is None:
            return False
        else:
            return True
    except SQLAlchemyError:
        return "Error al conectar a la base de datos"
