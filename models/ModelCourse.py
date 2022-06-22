from sqlalchemy import Table, Column, Integer, String
from config.ConfigDB import meta

courses = Table(
    'CAsignatura',
    meta,
    Column(
        'idAsignatura',
        Integer,
        primary_key=True
    ),
    Column(
        'clavAsignatura',
        String(10),
        nullable=False
    ),
    Column(
        'nomAsignatura',
        String(45),
        nullable=False
    )
)
