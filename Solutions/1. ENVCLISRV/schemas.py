
from models import get_v_livres
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import inspect

class LivreBase(BaseModel):
    titre: Optional[str] = None
    stock: Optional[int] = None

class LivreCreate(LivreBase):
    pass

class Livre(LivreBase):
    id: int

    class Config:
        from_attributes = True
        
def sqlalchemy_to_pydantic(table):
    attrs = {}
    annotations = {}

    for column in inspect(table).c:
        try:
            python_type = column.type.python_type
        except NotImplementedError:
            python_type = str  # fallback pour types complexes

        annotations[column.name] = python_type
        attrs[column.name] = Field(..., title=column.name, description=f"Type SQL: {column.type}")

    attrs['__annotations__'] = annotations  # ← essentiel pour Pydantic v2
    return type(f"{table.name}Schema", (BaseModel,), attrs)


def get_v_livres_schema():
    return sqlalchemy_to_pydantic(get_v_livres())