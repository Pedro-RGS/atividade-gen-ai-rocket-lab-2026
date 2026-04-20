from app.models.vendedor import Vendedor
from sqlalchemy.orm import Session
from app.utils.base_repository import BaseRepository

class VendedorRepository(BaseRepository[Vendedor]):

  def __init__(self, db: Session):
    super().__init__(db=db, model=Vendedor, pk_field="id_vendedor")
  