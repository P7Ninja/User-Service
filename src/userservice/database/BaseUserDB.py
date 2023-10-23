from . import schema


class BaseUserDB:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg

    def startup(self):pass
    def shutdown(self):pass
    def create_user(self, user: schema.UserCreate)-> int | None:pass
    def delete_user(self, id: int) -> bool:pass
    def update_user(self, user: schema.UserUpdate) -> bool:pass
    def get_user(self, id: int) -> schema.User | None:pass