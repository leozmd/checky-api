from sqlalchemy import Table, Column, Integer, String, Time
from config.ConfigDB import meta

schedules = Table(
    'CHorario',
    meta,
    Column(
        'idHorario',
        Integer,
        primary_key=True
    ),
    Column(
        'diaHorario',
        String(10),
        nullable=False
    ),
    Column(
        'iniHorario',
        Time,
        nullable=False
    ),
    Column(
        'finHorario',
        Time,
        nullable=False
    )
)
