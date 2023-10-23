from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class BaseUser(BaseModel):
    username: str
    email: str
    gender: str
    birthday: date

class Energy(BaseModel):
    calories: float
    fat: float
    carbohydrates: float
    protein: float
    
class UserCreate(BaseUser):
    target_energy: Energy
    password: str

class User(BaseUser):
    id: int
    created: datetime
    target_energy: Energy

class EnergyUpdate(BaseModel):
    calories: Optional[float] = None
    fat: Optional[float] = None
    carbohydrates: Optional[float] = None
    protein: Optional[float] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[date] = None
    target_energy: Optional[EnergyUpdate] = None
