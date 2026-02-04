from sqlalchemy import MetaData, Table, Column, Integer, String
from database import Base, engine

class Livre(Base):
    __tablename__ = "livre"
    __table_args__ = {"schema": "dbo"}

    id = Column("Id_Livre", Integer, primary_key=True, index=True)
    titre = Column("Titre", String(50), nullable=True)
    stock = Column("Stock", Integer, nullable=True)

metadata = MetaData(schema="dbo")
V_Livres = None

def get_v_livres():
    global V_Livres
    if V_Livres is None:
        V_Livres = Table("V_Livres", metadata, autoload_with=engine)
    return V_Livres