from sqlalchemy import Table, Column, Integer, String, ForeignKey
from config.ConfigDB import meta

users = Table(
    'MUsuario',
    meta,
    Column('idUsuario',
           Integer,
           primary_key=True),
    Column('nomUsuario',
           String(45),
           nullable=False),
    Column('appatUsuario',
           String(45),
           nullable=False),
    Column('apmatUsuario',
           String(45),
           nullable=False),
    Column('sexoUsuario',
           String(45),
           nullable=False),
    Column('matUsuario',
           String(45),
           nullable=False),
    Column('usuUsuario',
           String(45),
           nullable=False,
           unique=True),
    Column('passUsuario',
           String(255),
           nullable=False),
    Column('idRol',
           ForeignKey('CRol.idRol'),
           nullable=False
           ),
    Column('idEstado',
           ForeignKey('CEstado.idEstado'),
           nullable=False)
)
