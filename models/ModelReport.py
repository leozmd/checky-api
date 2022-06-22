from sqlalchemy import Table, Column, Integer, String, ForeignKey
from config.ConfigDB import meta

reports = Table(
    'MReporte',
    meta,
    Column(
        'idReporte',
        Integer,
        primary_key=True
    ),
    Column(
        'txtReporte',
        String,
        nullable=False
    ),
    Column(
        'edoReporte',
        String(45),
        nullable=False
    ),
    Column(
        'resReporte',
        String,
        nullable=False
    ),
    Column(
        'idUsuario',
        ForeignKey('MUsuario.idUsuario'),
        nullable=False
    )
)
