from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.avaliacoes_pedido_service import AvaliacaoPedidoService
from app.schemas.avaliacoes_pedido_schema import AvaliacaoListItemSchema

router = APIRouter(
  prefix="/avaliacoes",
  tags=["Avaliacoes"]
)

@router.get("/{id_produto}", status_code=status.HTTP_200_OK, response_model=AvaliacaoListItemSchema)
def list_produtos(id_produto: str, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
  service = AvaliacaoPedidoService(db)
  return service.get_paginated_reviews(id_produto, limit=limit, offset=offset)