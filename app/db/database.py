from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from dotenv import load_dotenv
import os 
# sqlite_file_name = "database.db"


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", default=None)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
    
) 


## The purpose of a sessionmaker is to provide  a factory  objects with  a fixed  configuration

DBSession = sessionmaker(
    autoflush=False,
    autocommit=False,    
    bind=engine

)



## This is being  used  for example  tocreates a database session for each request and closes it after
def get_db():
    db = DBSession()
    try:
        yield db
    
    finally:
        db.close()

Base = declarative_base()

