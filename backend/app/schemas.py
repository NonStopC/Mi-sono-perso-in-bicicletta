from pydantic import BaseModel
from typing import List, Optional

# Bicicletta schemas
class BiciclettaBase(BaseModel):
    tipo: str
    colore: str
    numero_ruote: int

class BiciclettaCreate(BiciclettaBase):
    pass

class Bicicletta(BiciclettaBase):
    id: int
    utente_id: int
    
    class Config:
        from_attributes = True


# Utente schemas
class UtenteBase(BaseModel):
    nome: str

class UtenteCreate(UtenteBase):
    pass

class Utente(UtenteBase):
    id: int
    biciclette: List[Bicicletta] = []
    
    class Config:
        from_attributes = True
