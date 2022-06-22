from sqlalchemy import Table, Column, Integer, String, ForeignKey
from config.ConfigDB import meta

answers = Table(
    'MRespuesta',
    meta,
    Column(
        'idRespuesta',
        Integer,
        primary_key=True
    ),
    Column(
        'txtRespuesta',
        String(255),
        nullable=False
    ),
    Column(
        'edoRespuesta',
        String(45),
        nullable=False
    ),
    Column(
        'idPregunta',
        ForeignKey('MPregunta.idPregunta'),
        nullable=False
    )
)
