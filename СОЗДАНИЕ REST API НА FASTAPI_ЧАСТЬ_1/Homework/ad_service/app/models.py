# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Float, func
from database import Base

class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    # ИСПРАВЛЕНИЕ: добавлено nullable=False, поле стало обязательным
    description = Column(String(1000), nullable=False)
    price = Column(Float, nullable=False)
    author = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "author": self.author,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }