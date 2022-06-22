from pydantic import BaseModel


class ScheduleClassroom(BaseModel):
    idHorario: int
    idClase: int
