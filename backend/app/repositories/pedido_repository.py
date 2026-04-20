from sqlalchemy.orm import Session
from typing import List
from app.models.pedido import Pedido
from app.utils.base_repository import BaseRepository

class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, db: Session):
      super().__init__(db=db, model=Pedido, pk_field="id_pedido")

    def find_by_consumidor(self, id_consumidor: str) -> List[Pedido]:
      return self.filter_by(id_consumidor=id_consumidor)

    def find_by_status(self, status: str) -> List[Pedido]:
      return self.filter_by(status=status)
    
    def find_atrasados(self) -> List[Pedido]:
      return self.filter_by(entrega_no_prazo="Não")