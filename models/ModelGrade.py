from sqlalchemy import Table, Column, Integer, String
from config.ConfigDB import meta

grades = Table(
    'CGrado',
    meta,
    Column(
        'idGrado',
        Integer,
        primary_key=True
    ),
    Column(
        'tipoGrado',
        String(45),
        nullable=False
    )
)
