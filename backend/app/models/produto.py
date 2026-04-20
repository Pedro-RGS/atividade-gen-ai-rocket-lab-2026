from typing import Optional

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id_produto: Mapped[str] = mapped_column(String(32), primary_key=True)
    nome_produto: Mapped[str] = mapped_column(String(255))
    categoria_produto: Mapped[Optional[str]] = mapped_column(String(100), ForeignKey("categoria_imagens.Categoria"), nullable=True)
    peso_produto_gramas: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    comprimento_centimetros: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    altura_centimetros: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    largura_centimetros: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # relationships
    itens_pedido: Mapped[list["ItemPedido"]] = relationship("ItemPedido", back_populates="produto", cascade="all, delete-orphan")
    imagem_categoria: Mapped["CategoriaImagem"] = relationship("CategoriaImagem", back_populates="produtos")