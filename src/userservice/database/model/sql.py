from sqlalchemy import func
from sqlalchemy.orm import declarative_base, DeclarativeBase, Mapped
from sqlalchemy import Column, ForeignKey, Integer, String, Double, Table, Text, Enum, DateTime, Date
from typing import List

Base: DeclarativeBase = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    created = Column(DateTime, default=func.now())

    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String, nullable=False)
    gender = Column(Enum("male", "female"), nullable=False)
    birthday = Column(Date, nullable=False)
    
    calories = Column(Double, nullable=False)
    fat = Column(Double, nullable=False)
    carbohydrates = Column(Double, nullable=False)
    protein = Column(Double, nullable=False)

