from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date
from config.ConfigDB import meta

lists = Table(
    'MLista',
    meta,
    Column(
        'idLista',
        Integer,
        primary_key=True
    ),
    Column(
        'diaLista',
        Date,
        nullable=False,
    ),
    Column(
        'idClase',
        ForeignKey('MClase.idClase'),
        nullable=False
    )
)
