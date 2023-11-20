import pytest
import shutil
from pytest import FixtureRequest
from pathlib import Path

from userservice.database import SQLUserDB
from userservice.database.schema import *
from datetime import date
from fastapi import HTTPException

@pytest.fixture
def db(request: FixtureRequest, tmp_path: Path):
    db_path = tmp_path / "db"
    db_path.mkdir()
    db_file = db_path / "db.sql"
    shutil.copyfile("./tests/test.db", db_file)
    db = SQLUserDB({"DB_CONN": f"sqlite:///{db_file}"})
    db.startup()
    def tearddown():
        db.shutdown()

    request.addfinalizer(tearddown)
    return db

def test_create_user(db: SQLUserDB):
    user = UserCreate(
        username="baugette",
        password="baugettesPassword5",
        email="bp@email.com",
        gender="female",
        birthday=date(1970, 1 , 1),
        target_energy=Energy(calories=2000, fat=60, carbohydrates=60, protein=50)
    )
    id = db.create_user(user)
    db_user = db.get_user(id).model_dump()
    
    for k, v in user.model_dump().items():
        if k in db_user:
            assert v == db_user[k]

def test_delete_user(db: SQLUserDB):
    user = db.get_user(5)
    assert user is not None
    db.delete_user(5)
    with pytest.raises(HTTPException) as e:
        user = db.get_user(5)
    assert e.value.status_code == 404

def test_update_user(db: SQLUserDB):
    with pytest.raises(HTTPException) as e:
        db.validate_user("user3", "pass2")
    assert e.value.status_code == 401
    db.update_user(4, UserUpdate(password="pass2"))
    id = db.validate_user("user3", "pass2")
    assert id == 4
    
def test_get_user(db: SQLUserDB):
    user = db.get_user(3)
    assert user.username == "user2"
    assert user.birthday == date(2003, 1, 1)

def test_validate_user(db: SQLUserDB):
    valid = db.validate_user("user5", "pass5")
    assert valid