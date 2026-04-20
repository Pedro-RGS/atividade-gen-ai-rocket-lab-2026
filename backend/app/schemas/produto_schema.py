from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from app.utils.pagination_schema import PaginationMetaSchema

class _StatisticsSchema(BaseModel):
    total_vendas: int
    total_avaliacoes: float
    media_nota: float

class _MedidasSchema(BaseModel):
    peso_produto_gramas: Optional[float]
    comprimento_centimetros: Optional[float]
    altura_centimetros: Optional[float]
    largura_centimetros: Optional[float]

class ProdutoCreateResponse(BaseModel):
    id_produto: str
    nome_produto: str
    categoria_produto: Optional[str] = None
    peso_produto_gramas: Optional[float] = Field(None, ge=0)
    comprimento_centimetros: Optional[float] = Field(None, ge=0)
    altura_centimetros: Optional[float] = Field(None, ge=0)
    largura_centimetros: Optional[float] = Field(None, ge=0)

class ProdutoCreateRequest(BaseModel):
    nome_produto: str
    categoria_produto: Optional[str] = None
    peso_produto_gramas: Optional[float] = Field(None, ge=0)
    comprimento_centimetros: Optional[float] = Field(None, ge=0)
    altura_centimetros: Optional[float] = Field(None, ge=0)
    largura_centimetros: Optional[float] = Field(None, ge=0)

class ProdutoListItemSchema(BaseModel):
    id_produto: str
    nome_produto: str
    categoria_produto: Optional[str]
    preco: float
    url_imagem: Optional[str] = None

class ProdutoDetalheResponse(ProdutoListItemSchema):
    medidas: _MedidasSchema
    estatisticas: _StatisticsSchema

class ProdutoListResponse(BaseModel):
    meta: PaginationMetaSchema
    data: List[ProdutoListItemSchema]

    model_config = ConfigDict(from_attributes=True)

class ProdutoUpdate(BaseModel):
    nome_produto: Optional[str] = None
    categoria_produto: Optional[str] = None
    peso_produto_gramas: Optional[float] = Field(None, ge=0)
    comprimento_centimetros: Optional[float] = Field(None, ge=0)
    altura_centimetros: Optional[float] = Field(None, ge=0)
    largura_centimetros: Optional[float] = Field(None, ge=0)
