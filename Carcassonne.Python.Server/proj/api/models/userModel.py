from sqlalchemy import Column, Integer, String
from ..db.base import Base

class userModel(Base):
    __tablename__ = "tblCategory"
    __table_args__ = {"schema": "dbo"}

    pkID = Column(Integer, primary_key=True)