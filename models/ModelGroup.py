from sqlalchemy import Table, Column, Integer, String
from config.ConfigDB import meta

groups = Table(
    'CGrupo',
    meta,
    Column(
        'idGrupo',
        Integer,
        primary_key=True
    ),
    Column(
        'tipoGrupo',
        String(2),
        nullable=False
    )
)
