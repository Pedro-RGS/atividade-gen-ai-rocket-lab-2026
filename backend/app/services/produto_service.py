from typing import List, Optional
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository
from fastapi import HTTPException, status
from app.schemas.produto_schema import ProdutoUpdate

class ProdutoService:
    def __init__(self, db: Session):
      self.repository = ProdutoRepository(db)

    def get_all(self, limit: int = 10, offset: int = 0, name: str = None, category: str = None) -> List[Produto]:
      produtos = self.repository.find_all(limit=limit, offset=offset, name=name, category=category)
      
      total_items = self.repository.count_all(name=name)
      current_page = (offset // limit) + 1
      total_pages = (total_items + limit - 1) // limit  # Cál
      
      return {
        "meta": {
          "total_items": total_items,
          "total_pages": total_pages,
          "current_page": current_page,
          "limit": limit,
          },
        "data": [{
          "id_produto": p.id_produto,
          "nome_produto": p.nome_produto,
          "categoria_produto": p.categoria_produto,
          "preco": p.itens_pedido[-1].preco_BRL if p.itens_pedido else 0.0,
          "url_imagem": p.imagem_categoria.Link if p.imagem_categoria else None
        }
        for p in produtos
      ]}

    def get_by_id(self, id_produto: str) -> Produto:
      produto = self.repository.find_by_id(id_produto)
      
      if not produto:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND, 
          detail=f"Produto com id {id_produto} não encontrado"
        )
      
      sales = produto.itens_pedido
      today_price = sales[-1].preco_BRL if sales else 0.0

      reviews = []
      for s in sales:
        if s.pedido and s.pedido.avaliacao_pedido:
          review = s.pedido.avaliacao_pedido
          reviews.append({
            "id_avaliacao": review.id_avaliacao,
            "avaliacao": review.avaliacao,
            "consumidor": s.pedido.consumidor.nome_consumidor if s.pedido.consumidor else "Desconhecido",
            "titulo_comentario": review.titulo_comentario,
            "comentario": review.comentario,
            "data_comentario": review.data_comentario,
          }) 
      
      return {
        "id_produto": produto.id_produto,
        "nome_produto": produto.nome_produto,
        "categoria_produto": produto.categoria_produto,
        "preco": today_price,
        "url_imagem": produto.imagem_categoria.Link if produto.imagem_categoria else None,
        "medidas": {
          "peso_produto_gramas": produto.peso_produto_gramas,
          "comprimento_centimetros": produto.comprimento_centimetros,
          "altura_centimetros": produto.altura_centimetros,
          "largura_centimetros": produto.largura_centimetros,
        },
        "estatisticas": {
          "total_vendas": len(sales),
          "total_avaliacoes": len(reviews),
          "media_nota": sum(a['avaliacao'] for a in reviews) / len(reviews) if reviews else 0
        },
        "reviews": reviews
      }
    
    def get_using_filter(self, **kwargs) -> List[Produto]:
      return self.repository.filter_by(**kwargs)

    def create(self, produto_data: dict) -> Produto:
      dict = produto_data.model_dump()

      new_produto = Produto(
        id_produto=uuid4().hex,
        **dict
        )
      
      created_produto = self.repository.create(new_produto)
      return {
        "id_produto": created_produto.id_produto,
        "nome_produto": created_produto.nome_produto,
        "categoria_produto": created_produto.categoria_produto,
        "peso_produto_gramas": created_produto.peso_produto_gramas,
        "comprimento_centimetros": created_produto.comprimento_centimetros,
        "altura_centimetros": created_produto.altura_centimetros,
        "largura_centimetros": created_produto.largura_centimetros
      }

    def update(self, id_produto: str, update_data: ProdutoUpdate) -> Produto:
      produto = self.repository.find_by_id(id_produto)
      
      if not produto:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND, 
          detail=f"Produto com id {id_produto} não encontrado"
        )
      
      dict = update_data.model_dump(exclude_unset=True)
        
      for key, value in dict.items():
        setattr(produto, key, value)
        
      return self.repository.update(produto)

    def delete(self, id_produto: str) -> None:
      produto = self.repository.find_by_id(id_produto)
      
      if not produto:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND, 
          detail=f"Produto com id {id_produto} não encontrado"
        )
      
      self.repository.delete(produto)