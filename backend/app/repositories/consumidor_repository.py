from app.models.consumidor import Consumidor
from sqlalchemy.orm import Session
from app.utils.base_repository import BaseRepository

class VendedorRepository(BaseRepository[Consumidor]):

  def __init__(self, db: Session):
    super().__init__(db=db, model=Consumidor, pk_field="id_consumidor")
  