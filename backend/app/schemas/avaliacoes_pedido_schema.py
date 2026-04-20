from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.utils.pagination_schema import PaginationMetaSchema

class AvaliacaoItemSchema(BaseModel):
  id_avaliacao: str
  avaliacao: int
  titulo_comentario: str
  comentario: str
  data_comentario: datetime
  nome_consumidor: str


class AvaliacaoListItemSchema(BaseModel):
  meta: PaginationMetaSchema
  data: List[AvaliacaoItemSchema]

  model_config = ConfigDict(from_attributes=True)