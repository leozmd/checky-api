from sqlalchemy import Table, Column, Integer, String, ForeignKey
from config.ConfigDB import meta

questions = Table(
    'MPregunta',
    meta,
    Column(
        'idPregunta',
        Integer,
        primary_key=True
    ),
    Column(
        'txtPregunta',
        String,
        nullable=False
    ),
    Column(
        'idMiembro',
        ForeignKey('MMiembro.idMiembro'),
        nullable=False
    )
)
