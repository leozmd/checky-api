from sqlalchemy import Table, Column, Integer, ForeignKey
from config.ConfigDB import meta

classroom_schedules = Table(
    'RHorarioClase',
    meta,
    Column(
        'idHorarioClase',
        Integer,
        primary_key=False
    ),
    Column(
        'idHorario',
        ForeignKey('CHorario.idHorario'),
        nullable=False
    ),
    Column(
        'idClase',
        ForeignKey('MClase.idClase'),
        nullable=False
    )
)
