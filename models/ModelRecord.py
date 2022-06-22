from sqlalchemy import Table, Column, Integer, ForeignKey, Date, Time
from config.ConfigDB import meta

records = Table(
    'MRegistro',
    meta,
    Column(
        'idRegistro',
        Integer,
        primary_key=True
    ),
    Column(
        'diaRegistro',
        Date,
        nullable=False,
    ),
    Column(
        'horaRegistro',
        Time,
        nullable=False,
    ),
    Column(
        'idMiembro',
        ForeignKey('MMiembro.idMiembro'),
        nullable=False
    ),
    Column(
        'idLista',
        ForeignKey('MLista.idLista'),
        nullable=False
    )
)
