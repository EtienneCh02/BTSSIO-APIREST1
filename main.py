from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import database
import schemas
import models
#from database import get_db
import crud
from models import V_Livres
from schemas import V_LivresSchema
from typing import List
import logging

logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("api_logger")
app = FastAPI(title="TP API - FastAPI + SQL Server")

from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"{request.client.host} "
        f"{request.method} "
        f"{request.url.path} "
        f"status={response.status_code} "
        f"time={duration:.3f}s"
    )

    return response

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

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Clé API manquante ou invalide"
        )
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
def read_v_livres(  db: Session = Depends(get_db),
    _: None = Depends(verify_api_key)):
    result = db.execute(V_Livres.select()).mappings().all()  # ✅ ici
    return list(result)  # chaque élément est déjà un dict compatible Pydantic