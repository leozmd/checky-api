from sqlalchemy import Table, Column, Integer, String, ForeignKey
from config.ConfigDB import meta

choices = Table(
    'MEleccion',
    meta,
    Column(
        'idEleccion',
        Integer,
        primary_key=True
    ),
    Column(
        'idRespuesta',
        ForeignKey('MRespuesta.idRespuesta'),
        nullable=False
    )
)
