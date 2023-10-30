from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class BaseUser(BaseModel):
    username: str = Field(examples=["John123"])
    email: str = Field(examples=["example@email.com"])
    gender: str = Field(examples=["male"])
    birthday: date = Field(examples=[date(1970,1, 1)])

class Energy(BaseModel):
    calories: float = Field(examples=[2000])
    fat: float = Field(examples=[60])
    carbohydrates: float = Field(examples=[60])
    protein: float = Field(examples=[60])
    
class UserCreate(BaseUser):
    target_energy: Energy
    password: str = Field(examples=["secretkitten65"])

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
    password: Optional[str] = None
    email: Optional[str] = None
    birthday: Optional[date] = None
    target_energy: Optional[EnergyUpdate] = None

class Login(BaseModel):
    username: str
    password: str