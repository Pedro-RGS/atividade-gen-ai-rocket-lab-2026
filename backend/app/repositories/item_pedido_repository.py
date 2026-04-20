from app.models.item_pedido import ItemPedido
from sqlalchemy.orm import Session
from app.utils.base_repository import BaseRepository
from sqlalchemy import select
from typing import Optional

class ItemPedidoRepository(BaseRepository[ItemPedido]):

  def __init__(self, db: Session):
    super().__init__(db=db, model=ItemPedido)

  def findy_by_id(self, id_pedido: str, id_item: int) -> Optional[ItemPedido]:
    stmt = select(self.model).where(
      self.model.id_pedido == id_pedido,
      self.model.id_item == id_item
    )
    return self.db.execute(stmt).scalar_one_or_none()
  
  def find_by_pedido(self, id_pedido: str):
    return self.filter_by(id_pedido=id_pedido)
  
  def find_by_produto(self, id_produto: str):
    return self.filter_by(id_produto=id_produto)
  