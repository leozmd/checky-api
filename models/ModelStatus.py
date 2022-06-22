from sqlalchemy import Table, Column, Integer, String
from config.ConfigDB import meta

statuses = Table(
    'CEstado',
    meta,
    Column(
        'idEstado',
        Integer,
        primary_key=True
    ),
    Column(
        'tipoEstado',
        String(45),
        nullable=False,
    ),
    Column(
        'resEstado',
        Integer,
        nullable=False
    )
)
