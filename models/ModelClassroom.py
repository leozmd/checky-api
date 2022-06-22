from sqlalchemy import Table, Column, Integer, String, ForeignKey
from config.ConfigDB import meta

classrooms = Table(
    'MClase',
    meta,
    Column(
        'idClase',
        Integer,
        primary_key=True
    ),
    Column(
        'idCarrera',
        ForeignKey('CCarrera.idCarrera'),
        nullable=False
    ),
    Column(
        'idGrado',
        ForeignKey('CGrado.idGrado'),
        nullable=False
    ),
    Column(
        'idTurno',
        ForeignKey('CTurno.idTurno'),
        nullable=False
    ),
    Column(
        'idGrupo',
        ForeignKey('CGrupo.idGrupo'),
        nullable=False
    ),
    Column(
        'idAsignatura',
        ForeignKey('CAsignatura.idAsignatura'),
        nullable=False
    )
)
