from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.produto_service import ProdutoService
from app.schemas.produto_schema import ProdutoListResponse, ProdutoDetalheResponse, ProdutoUpdate, ProdutoCreateRequest, ProdutoCreateResponse

router = APIRouter(
  prefix="/produtos",
  tags=["Produtos"]
)

@router.get("/{id_produto}", status_code=status.HTTP_200_OK, response_model=ProdutoDetalheResponse)
def get_produto_detalhes(id_produto: str, db: Session = Depends(get_db)):
  service = ProdutoService(db)
  return service.get_by_id(id_produto)

@router.get("/", status_code=status.HTTP_200_OK, response_model=ProdutoListResponse)
def list_produtos(limit: int = 10, offset: int = 0, name: str = None, category: str = None, db: Session = Depends(get_db)):
  service = ProdutoService(db)
  return service.get_all(limit=limit, offset=offset, name=name, category=category)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProdutoCreateResponse)
def create_produto(produto_data: ProdutoCreateRequest, db: Session = Depends(get_db)):
  service = ProdutoService(db)
  return service.create(produto_data)

@router.patch("/{id_produto}", status_code=status.HTTP_200_OK, response_model=ProdutoCreateResponse)
def update_produto(id_produto: str, update_data: ProdutoUpdate, db: Session = Depends(get_db)):
  service = ProdutoService(db)
  return service.update(id_produto, update_data)

@router.delete("/{id_produto}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produto(id_produto: str, db: Session = Depends(get_db)):
  service = ProdutoService(db)
  service.delete(id_produto)
  return None