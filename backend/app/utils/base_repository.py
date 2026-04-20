from typing import Any, TypeVar, Generic, Optional, Type, List

from sqlalchemy.orm import Session
from sqlalchemy import select, func

T = TypeVar("T")

class BaseRepository(Generic[T]):

  def __init__(self, db: Session, model: Type[T], pk_field: str = "id"):
    self.db = db
    self.model = model
    self.pk_field = pk_field
  
  def find_by_id(self, id_value: Any) -> Optional[T]:
    stmt = select(self.model).filter(getattr(self.model, self.pk_field) == id_value)
    return self.db.execute(stmt).scalar_one_or_none()

  def find_all(self, limit: int = 100, offset: int = 0) -> List[T]:
    stmt = select(self.model).limit(limit).offset(offset)
    return self.db.execute(stmt).scalars().all()
  
  def count(self) -> int:
    stmt = select(func.count()).select_from(self.model)
    return self.db.execute(stmt).scalar()

  def filter_by(self, **kwargs) -> List[T]:
    stmt = select(self.model).filter_by(**kwargs)
    return self.db.execute(stmt).scalars().all()
  
  def create(self, obj: T) -> T:
    self.db.add(obj)
    self.db.commit()
    self.db.refresh(obj)
    return obj
  
  def update(self, obj: T) -> T:
    self.db.merge(obj)
    self.db.commit()
    self.db.refresh(obj)
    return obj
  
  def delete(self, obj: T) -> None:
    self.db.delete(obj)
    self.db.commit()