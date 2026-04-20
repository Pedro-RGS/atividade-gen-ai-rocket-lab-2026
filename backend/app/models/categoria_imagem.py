from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CategoriaImagem(Base):
    __tablename__ = "categoria_imagens"

    Categoria: Mapped[str] = mapped_column(String(100), primary_key=True)
    Link: Mapped[str] = mapped_column(String(255), nullable=False)

    # relationships
    produtos: Mapped[list["Produto"]] = relationship("Produto", back_populates="imagem_categoria")