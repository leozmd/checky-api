from sqlalchemy import Table, Column, Integer, String
from config.ConfigDB import meta

shifts = Table(
    'CTurno',
    meta,
    Column(
        'idTurno',
        Integer,
        primary_key=True
    ),
    Column(
        'nomTurno',
        String(45),
        nullable=False
    )
)
