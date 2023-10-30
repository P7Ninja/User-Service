import pytest
import shutil
import json
from pytest import FixtureRequest
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient

from userservice.database import SQLUserDB
from userservice.database.schema import *
from userservice import UserService

@pytest.fixture
def client(request: FixtureRequest, tmp_path: Path):
    db_path = tmp_path / "db"
    db_path.mkdir()
    db_file = db_path / "db.sql"
    shutil.copyfile("./tests/test.db", db_file)

    db = SQLUserDB({"DB_CONN": f"sqlite:///{db_file}"})
    app = FastAPI()
    service = UserService(app, db, dict())
    db.startup()
    service.configure_routes()
    request.addfinalizer(lambda: db.shutdown())

    return TestClient(app)

def test_create_user(client: TestClient):
    user = {
        "username": "baugette", 
        "password": "baugettesPassword5",
        "email":"bp@email.com",
        "gender":"female",
        "birthday": "1970-01-01",
        "target_energy": {
                "calories": 2000,
                "fat": 60,
                "carbohydrates": 60,
                "protein": 50
            },
        }

    res = client.post("/user", content=json.dumps(user))
    assert res.status_code == 201
    assert res.json()


def test_delete_user(client: TestClient):
    res = client.delete("/user/5")
    assert res.json()

def test_update_user(client: TestClient):
    res = client.put("/user/5", content=json.dumps({"email":"myemail@mail.com"}))
    user = client.get("/user/5")
    assert res.status_code == 200
    assert res.json()
    assert user.json()["email"] == "myemail@mail.com"

def test_get_user(client: TestClient):
    res = client.get("/user/6")
    user = res.json()

    assert res.status_code == 200
    assert user["username"] == "user5"

def test_validate_user(client: TestClient):
    res = client.post("/validate", content=json.dumps({"username": "user9", "password": "pass9"}))
    assert res.status_code == 200
    assert res.json() 

def test_default(client: TestClient):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "User-Service"}