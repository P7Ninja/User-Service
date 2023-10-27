from . import schema


class BaseUserDB:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg

    def startup(self):pass
    def shutdown(self):pass
    def create_user(self, user: schema.UserCreate):pass
    def delete_user(self, id: int):pass
    def update_user(self, id: int, user: schema.UserUpdate):pass
    def get_user(self, id: int) -> schema.User:pass
    def validate_user(self, username: str, password: str):pass