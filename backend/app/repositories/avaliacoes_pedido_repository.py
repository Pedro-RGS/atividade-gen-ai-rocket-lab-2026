from app.models.avaliacao_pedido import AvaliacaoPedido
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from sqlalchemy.orm import Session, joinedload
from app.utils.base_repository import BaseRepository

class AvaliacaoPedidoRepository(BaseRepository[AvaliacaoPedido]):

  def __init__(self, db: Session):
    super().__init__(db=db, model=AvaliacaoPedido, pk_field="id_avaliacao")
  
  def get_by_product(self, id_produto: str, limit: int = 10, offset: int = 0):
    return (
      self.db.query(self.model)
      .join(Pedido, self.model.id_pedido == Pedido.id_pedido)
      .join(ItemPedido, Pedido.id_pedido == ItemPedido.id_pedido)
      .filter(ItemPedido.id_produto == id_produto)
      .options(joinedload(self.model.pedido).joinedload(Pedido.consumidor))
      .distinct()
      .limit(limit)
      .offset(offset)
      .all()
    )
  
  def count_by_product(self, id_produto: str) -> int:
    return (
      self.db.query(self.model)
      .join(Pedido, self.model.id_pedido == Pedido.id_pedido)
      .join(ItemPedido, Pedido.id_pedido == ItemPedido.id_pedido)
      .filter(ItemPedido.id_produto == id_produto)
      .distinct()
      .count()
    )