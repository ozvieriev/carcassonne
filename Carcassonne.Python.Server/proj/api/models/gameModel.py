from sqlalchemy import Column, Integer, UUID, String, JSON, DateTime
from ..db.base import Base

class gameModel(Base):
    __tablename__ = "game"
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String, nullable=False, default="{}")
    createDateUtc = Column(DateTime, nullable=False)