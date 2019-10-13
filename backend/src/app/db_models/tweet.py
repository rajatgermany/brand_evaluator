from app.db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

class Tweet(Base):
    id = Column(Integer, primary_key=True, index=True)
    sentiment = Column(String, index=True)
    text = Column(String, index=True)
    
