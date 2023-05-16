from sqlalchemy import Column, DateTime, Integer, String, Boolean, JSON, Double
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RealEstates(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "real_estates"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    description = Column(String)
    total_price = Column(Double)
    price = Column(Double)
    rent = Column(Double)
    currency = Column(String)
    area = Column(Double)
    rooms = Column(Integer)
    deposit = Column(Double)
    floor = Column(String)
    type = Column(String)
    status = Column(String)
    region = Column(String)