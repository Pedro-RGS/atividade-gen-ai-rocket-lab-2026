from sqlalchemy.orm import Session, joinedload
from app.utils.base_repository import BaseRepository
from app.models.produto import Produto

class ProdutoRepository(BaseRepository[Produto]):
  def __init__(self, db: Session):
    super().__init__(db=db, model=Produto, pk_field="id_produto")
  
  def find_by_id(self, id_produto: str):
    return self.db.query(self.model)\
        .options(joinedload(self.model.itens_pedido))\
        .filter(self.model.id_produto == id_produto)\
        .first()

  def find_all(self, limit=100, offset=0, name: str = None, category: str = None):
    query = self.db.query(self.model)
    
    if name:
      query = query.filter(self.model.nome_produto.ilike(f"%{name}%"))
    
    if category:
      query = query.filter(self.model.categoria_produto == category)
    
    return query.limit(limit).offset(offset).all()
  
  def count_all(self, name: str = None) -> int:
    query = self.db.query(self.model)
    
    if name:
        query = query.filter(self.model.nome_produto.ilike(f"%{name}%"))
        
    return query.count()
