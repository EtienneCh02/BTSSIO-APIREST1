import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

#Variables d'environnement

DB_SERVER='GIBCYWIN\\SQLEXPRESS01'
DB_NAME='BookCo'
DB_USER='APIREST1'
DB_PASSWORD='7zHDG4Ybj6y3m3'


#load_dotenv()
 
#server = os.getenv("DB_SERVER")
#database = os.getenv("DB_NAME")
#user = os.getenv("DB_USER")
#password = os.getenv("DB_PASSWORD")
server = DB_SERVER
database = DB_NAME
user = DB_USER
password = DB_PASSWORD
 
SQLALCHEMY_DATABASE_URL = (
    f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"
)
 
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()