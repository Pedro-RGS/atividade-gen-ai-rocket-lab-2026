from sqlalchemy.orm import Session
from app.repositories.avaliacoes_pedido_repository import AvaliacaoPedidoRepository

class AvaliacaoPedidoService:
    def __init__(self, db: Session):
        self.repository = AvaliacaoPedidoRepository(db)

    def get_paginated_reviews(self, id_produto: str, limit: int = 5, offset: int = 0):
      reviews = self.repository.get_by_product(id_produto, limit, offset)

      total_items = self.repository.count_by_product(id_produto)
      current_page = (offset // limit) + 1
      total_pages = (total_items + limit - 1) // limit

      return {
        "meta": {
          "total_items": total_items,
          "total_pages": total_pages,
          "current_page": current_page,
          "limit": limit
        },
        "data": [
          {
            "id_avaliacao": r.id_avaliacao,
            "avaliacao": r.avaliacao,
            "titulo_comentario": r.titulo_comentario,
            "comentario": r.comentario,
            "data_comentario": r.data_comentario,
            "nome_consumidor": r.pedido.consumidor.nome_consumidor if r.pedido.consumidor else "Anônimo"
          }
          for r in reviews
        ]
      }