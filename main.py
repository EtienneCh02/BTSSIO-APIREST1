from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database
import schemas
import models
#from database import get_db
import crud
from models import V_Livres
from schemas import V_LivresSchema
from typing import List

app = FastAPI(title="TP API - FastAPI + SQL Server")

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.get("/v_livres", response_model=List[V_LivresSchema])
def read_v_livres(db: Session = Depends(get_db)):
    result = db.execute(V_Livres.select()).mappings().all()  # ✅ ici
    return list(result)  # chaque élément est déjà un dict compatible Pydantic