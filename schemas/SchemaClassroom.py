from pydantic import BaseModel


class Classroom(BaseModel):
    idCarrera: int
    idGrado: int
    idTurno: int
    idGrupo: int
    idAsignatura: int
