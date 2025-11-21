from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List


from . import models
from . import schemas
from .database import engine, get_db


# Crea le tabelle nel database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Biciclette API")


# Configurazione CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ENDPOINTS UTENTI =====

@app.post("/utenti/", response_model=schemas.Utente)
def crea_utente(utente: schemas.UtenteCreate, db: Session = Depends(get_db)):
    db_utente = db.query(models.Utente).filter(models.Utente.nome == utente.nome).first()
    if db_utente:
        raise HTTPException(status_code=400, detail="Nome già registrato")
    
    nuovo_utente = models.Utente(nome=utente.nome)
    db.add(nuovo_utente)
    db.commit()
    db.refresh(nuovo_utente)
    return nuovo_utente


@app.get("/utenti/{nome}", response_model=schemas.Utente)
def login_utente(nome: str, db: Session = Depends(get_db)):
    utente = db.query(models.Utente).filter(models.Utente.nome == nome).first()
    if not utente:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return utente


@app.get("/utenti/", response_model=List[schemas.Utente])
def lista_utenti(db: Session = Depends(get_db)):
    return db.query(models.Utente).all()


# ===== ENDPOINTS BICICLETTE =====

@app.post("/utenti/{utente_id}/biciclette/", response_model=schemas.Bicicletta)
def aggiungi_bicicletta(
    utente_id: int,
    bicicletta: schemas.BiciclettaCreate,
    db: Session = Depends(get_db)
):
    utente = db.query(models.Utente).filter(models.Utente.id == utente_id).first()
    if not utente:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    
    nuova_bici = models.Bicicletta(
        **bicicletta.dict(),
        utente_id=utente_id
    )
    db.add(nuova_bici)
    db.commit()
    db.refresh(nuova_bici)
    return nuova_bici


@app.get("/biciclette/", response_model=List[schemas.Bicicletta])
def lista_biciclette(db: Session = Depends(get_db)):
    return db.query(models.Bicicletta).all()


@app.get("/biciclette/{bicicletta_id}", response_model=schemas.Bicicletta)
def dettaglio_bicicletta(bicicletta_id: int, db: Session = Depends(get_db)):
    bici = db.query(models.Bicicletta).filter(models.Bicicletta.id == bicicletta_id).first()
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicletta non trovata")
    return bici


@app.delete("/biciclette/{bicicletta_id}")
def elimina_bicicletta(bicicletta_id: int, db: Session = Depends(get_db)):
    bici = db.query(models.Bicicletta).filter(models.Bicicletta.id == bicicletta_id).first()
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicletta non trovata")
    
    db.delete(bici)
    db.commit()
    return {"detail": "Bicicletta eliminata"}


@app.put("/utenti/{utente_id}", response_model=schemas.Utente)
def aggiorna_utente(
    utente_id: int,
    utente: schemas.UtenteCreate,
    db: Session = Depends(get_db)
):
    db_utente = db.query(models.Utente).filter(models.Utente.id == utente_id).first()
    if not db_utente:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    
    db_utente.nome = utente.nome
    db.commit()
    db.refresh(db_utente)
    return db_utente


@app.delete("/utenti/{utente_id}")
def elimina_utente(utente_id: int, db: Session = Depends(get_db)):
    utente = db.query(models.Utente).filter(models.Utente.id == utente_id).first()
    if not utente:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    
    db.delete(utente)
    db.commit()
    return {"detail": "Utente eliminato"}


@app.put("/biciclette/{bicicletta_id}", response_model=schemas.Bicicletta)
def aggiorna_bicicletta(
    bicicletta_id: int,
    bicicletta: schemas.BiciclettaCreate,
    db: Session = Depends(get_db)
):
    db_bici = db.query(models.Bicicletta).filter(models.Bicicletta.id == bicicletta_id).first()
    if not db_bici:
        raise HTTPException(status_code=404, detail="Bicicletta non trovata")
    
    db_bici.tipo = bicicletta.tipo
    db_bici.colore = bicicletta.colore
    db_bici.numero_ruote = bicicletta.numero_ruote
    db.commit()
    db.refresh(db_bici)
    return db_bici
