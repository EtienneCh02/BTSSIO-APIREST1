from sqlalchemy.orm import Session
import models
import schemas

def get_livres(db: Session):
    return db.query(models.Livre).all()

def get_livre(db: Session, livre_id: int):
    return db.query(models.Livre).filter(models.Livre.id == livre_id).first()

def create_livre(db: Session, livre: schemas.LivreCreate):
    db_livre = models.Livre(
        titre=livre.titre,
        stock=livre.stock
    )
    db.add(db_livre)
    db.commit()
    db.refresh(db_livre)
    return db_livre

def delete_livre(db: Session, livre_id: int):
    livre = get_livre(db, livre_id)
    if livre:
        db.delete(livre)
        db.commit()
    return livre
