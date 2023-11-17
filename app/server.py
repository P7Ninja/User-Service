
from fastapi import FastAPI

from userservice import UserService
from userservice.database import SQLUserDB

import os

cfg = os.environ

app = FastAPI()

service = UserService(app, SQLUserDB(cfg), cfg)

service.configure_database()
service.configure_routes()
