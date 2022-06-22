from sqlalchemy import create_engine, MetaData

engine = create_engine(
    "mysql+pymysql://root:Zamudio_3108@localhost:3306/checky")
meta = MetaData()

conn = engine.connect()
