from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import database
import schemas
import models
#from database import get_db
import crud
from models import get_v_livres
from schemas import get_v_livres_schema
from typing import List
import warnings
from sqlalchemy.exc import SAWarning

warnings.filterwarnings(
    "ignore",
    message="Unrecognized server version info.*",
    category=SAWarning
)
app = FastAPI(title="TP API - FastAPI + SQL Server")

API_KEY = "tp-secret-key"

@app.get("/public")
def public():
    return {"message": "Accès public"}

@app.get("/protected")
def protected(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Clé API manquante ou invalide"
        )
    return {"message": "Accès autorisé"}
    
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Clé API manquante ou invalide"
        )
        

@app.get("/v_livres")
def read_v_livres(
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    table = get_v_livres()
    V_LivresSchema = get_v_livres_schema()
    result = db.execute(table.select()).mappings().all()
    return [V_LivresSchema(**r) for r in result]
    
@app.get("/livres", response_model=list[schemas.Livre])
def read_livres(db: Session = Depends(get_db)):
    return crud.get_livres(db)

@app.post("/livres", response_model=schemas.Livre)
def create_livre(livre: schemas.LivreCreate, db: Session = Depends(get_db)):
    return crud.create_livre(db, livre)

@app.get("/livres/{livre_id}", response_model=schemas.Livre)
def read_livre(livre_id: int, db: Session = Depends(get_db)):
    db_livre = crud.get_livre(db, livre_id)
    if not db_livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return db_livre

@app.delete("/livres/{livre_id}")
def delete_livre(livre_id: int, db: Session = Depends(get_db)):
    if not crud.delete_livre(db, livre_id):
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return {"message": "Livre supprimé"}