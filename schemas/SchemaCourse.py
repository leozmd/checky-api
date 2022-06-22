from pydantic import BaseModel


class Course(BaseModel):
    clavAsignatura: str
    nomAsignatura: str
