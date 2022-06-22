from sqlalchemy import ForeignKey, Table, Column, Integer, String
from config.ConfigDB import meta

members = Table(
    'MMiembro',
    meta,
    Column(
        'idMiembro',
        Integer,
        primary_key=True
    ),
    Column(
        'idUsuario',
        ForeignKey('MUsuario.idUsuario'),
        nullable=False
    ),
    Column(
        'idClase',
        ForeignKey('MClase.idClase'),
        nullable=False
    )
)
