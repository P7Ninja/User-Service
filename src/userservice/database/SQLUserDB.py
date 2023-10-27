from sqlalchemy import create_engine, func, or_, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, session
from .BaseUserDB import BaseUserDB
from .model import sql as model
from . import schema
import bcrypt
from fastapi import HTTPException, status
import re

class SQLUserDB(BaseUserDB):
    def __init__(self, cfg: dict) -> None:
        super().__init__(cfg)

        self.__engine = None
        self.__local = None
        self.__db = None

    def startup(self, connect_args: dict=dict()):
        self.__engine = create_engine(self.cfg["DB_CONN"], connect_args=connect_args)
        self.__local = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
        self.__db = self.__local()
        model.Base.metadata.create_all(self.__engine)

    def shutdown(self):
        session.close_all_sessions()
        self.__engine.dispose()

    def create_user(self, user: schema.UserCreate):
        try:
            exists = self.__db.query(model.User).filter(model.User.username == user.username).first()
            if exists is not None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{user.username} already exists")
            
            if user.gender not in ["male", "female"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{user.gender} is not a valid gender")

            if not self.__validate_email(user.email):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{user.email} is not a valid email")

            db_user = model.User(
                username = user.username,
                password = self.__hash(user.password),
                email = user.email,
                gender = user.gender,
                birthday = user.birthday,
                calories = user.target_energy.calories,
                fat = user.target_energy.fat,
                carbohydrates = user.target_energy.carbohydrates,
                protein = user.target_energy.protein
            )
            self.__db.add(db_user)
            self.__db.commit()
            self.__db.refresh(db_user)
        except SQLAlchemyError as e:
            self.__db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        return db_user.id

    def delete_user(self, id: int):
        try:
            db_user = self.__db.query(model.User).filter(model.User.id == id).first()
            if db_user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no user with {id} exists")
            self.__db.delete(db_user)
            self.__db.commit()
        except SQLAlchemyError as e:
            self.__db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        
    def update_user(self, id: int, user: schema.UserUpdate):
        try:
            db_user = self.__db.query(model.User).filter(model.User.id == id).first()
            if db_user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no user with {id} exists")
            
            user_dict = user.model_dump()
            if user_dict["target_energy"] is not None:
                user_dict = {**user_dict, **user_dict["target_energy"]}
                del user_dict["target_energy"]
            for k, v in user_dict.items():
                if k == "password" and v is not None:
                    setattr(db_user, k, self.__hash(v))
                    continue
                if v is None:
                    continue
                setattr(db_user, k, v)
            self.__db.commit()
        except SQLAlchemyError as e:
            self.__db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

    def get_user(self, id: int):
        try:
            db_user = self.__db.query(model.User).filter(model.User.id == id).first()
            if db_user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no user with {id} exists")
            
            return schema.User(
                id = db_user.id,
                created = db_user.created,
                username= db_user.username,
                email=db_user.email,
                gender = db_user.gender,
                birthday= db_user.birthday,
                target_energy=schema.Energy(
                    calories = db_user.calories,
                    fat = db_user.fat,
                    carbohydrates=db_user.carbohydrates,
                    protein=db_user.protein
                )
            )

        except SQLAlchemyError as e:
            self.__db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

    def validate_user(self, username: str, password: str) -> int | None:
        exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"incorrect username or password")
        db_user = self.__db.query(model.User).filter(model.User.username == username).first()
        if db_user is None:
            raise exception
        is_valid = bcrypt.checkpw(password.encode(), db_user.password)
        if not is_valid:
            raise exception
        return db_user.id



    def __hash(self, password: str):
        return bcrypt.hashpw(
            password.encode(), 
            bcrypt.gensalt(rounds=self.cfg.get("SALT", 12))
            )
    
    def __validate_email(self, email: str):  
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None 
