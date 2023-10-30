
from fastapi import FastAPI
from dotenv import dotenv_values

from userservice import UserService
from userservice.database import SQLUserDB

cfg = dotenv_values(".env")

app = FastAPI()

service = UserService(app, SQLUserDB(cfg), cfg)

service.configure_database()
service.configure_routes()
