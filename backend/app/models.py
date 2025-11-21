from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Utente(Base):
    __tablename__ = "utenti"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    
    biciclette = relationship("Bicicletta", back_populates="proprietario")


class Bicicletta(Base):
    __tablename__ = "biciclette"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    colore = Column(String, nullable=False)
    numero_ruote = Column(Integer, nullable=False)
    utente_id = Column(Integer, ForeignKey("utenti.id"))
    
    proprietario = relationship("Utente", back_populates="biciclette")
