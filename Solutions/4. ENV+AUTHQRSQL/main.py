from fastapi import FastAPI, Depends, HTTPException, Header, Request, APIRouter, status
import auth
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from auth import authenticate_user, create_access_token
from dependencies import get_current_user
from datetime import timedelta

from sqlalchemy.orm import Session
import database
import schemas
import models
import time
#from database import get_db
import crud
from models import get_v_livres
from schemas import get_v_livres_schema
from typing import List
import warnings
from sqlalchemy.exc import SAWarning

##JOURNALISATION
import logging

logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("api_logger")

warnings.filterwarnings(
    "ignore",
    message="Unrecognized server version info.*",
    category=SAWarning
)

app = FastAPI(title="TP API - FastAPI + SQL Server")
app.include_router(auth.router)
##SECURISATION API KEY
API_KEY = "tp-secret-key"
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

##SECURITE SQL INTEGREE
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


router = APIRouter(tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 60

## QRCODE intégré
# --- récupérer le secret depuis DB ---
def get_totp_secret(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user.totp_secret if user else None

# --- enregistrer le secret dans DB ---
def save_totp_secret(db: Session, username: str, secret: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.totp_secret = secret
        db.commit()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login ou mot de passe incorrect"
        )

    token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
## APPELS DES CLASSES
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
    #_: None = Depends(verify_api_key)
    user = Depends(get_current_user)
    
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