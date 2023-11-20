
from fastapi import FastAPI

from userservice import UserService
from userservice.database import SQLUserDB
from dotenv import dotenv_values

import os

if os.path.exists(".env"):
    cfg = dotenv_values(".env")

cfg["DB_CONN"] = os.environ.get("DB_CONN", cfg["DB_CONN"])

app = FastAPI()

service = UserService(app, SQLUserDB(cfg), cfg)

service.configure_database()
service.configure_routes()
