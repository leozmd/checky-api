from sqlalchemy import Table, Column, Integer, String
from config.ConfigDB import meta

roles = Table(
    'CRol',
    meta,
    Column(
        'idRol',
        Integer,
        primary_key=True
    ),
    Column(
        'tipoRol',
        String(45),
        nullable=False,
    )
)
