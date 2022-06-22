from sqlalchemy import Table, Column, Integer, String
from config.ConfigDB import meta

careers = Table(
    'CCarrera',
    meta,
    Column(
        'idCarrera',
        Integer,
        primary_key=True
    ),
    Column(
        'nomCarrera',
        String(45),
        nullable=False
    )
)
