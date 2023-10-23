from fastapi import FastAPI, HTTPException
from .database import schema, BaseUserDB

class UserService:
    def __init__(self, app: FastAPI, db: BaseUserDB, cfg: dict) -> None:
        self.__app = app
        self.__cfg = cfg
        self.__db = db

    def configure_database(self):
        @self.__app.on_event("startup")
        def startup():
            self.__db.startup()
        
        @self.__app.on_event("shutdown")
        def shutdown():
            self.__db.shutdown()

    def configure_routes(self):
        self.__app.add_api_route("/user", self.create_user, methods=["POST"], status_code=201)
        self.__app.add_api_route("/user/{id}", self.delete_user, methods=["DELETE"], status_code=200)
        self.__app.add_api_route("/user/{id}", self.update_user, methods=["PUT"], status_code=200)
        self.__app.add_api_route("/user/{id}", self.get_user, methods=["GET"], status_code=200)
        self.__app.add_api_route("/validate", self.validate_user, methods=["POST"], status_code=200)
        self.__app.add_api_route("/", lambda: {"message": "User-Service"}, methods=["GET"], status_code=200)

    async def create_user(self, user: schema.UserCreate)-> bool:
        res = self.__db.create_user(user)
        if res is None:
            raise HTTPException(status_code=500, detail="Something went wrong!")
        return True

    async def delete_user(self, id: int) -> bool:
        if not self.__db.delete_user(id):
            raise HTTPException(status_code=400, detail="No ID corresponding to user")
        return True
    
    async def update_user(self, user: schema.UserUpdate) -> bool:
        if not self.__db.update_user(user):
            raise HTTPException(status_code=500, detail="Something went wrong!")
        return True
    
    async def get_user(self, id: int) -> schema.User:
        user = self.__db.get_user(id)
        if user is None:
            raise HTTPException(status_code=400, detail="No ID corresponding to user")
        return user
    
    async def validate_user(self, login: schema.Login) -> bool:
        return self.__db.validate_user(login.username, login.password)