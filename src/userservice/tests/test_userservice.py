import pytest
from ..userservice import InsertUserInfo, DeleteUser, GetUser


@pytest.fixture
def test_GetUser(userID):
    pass


@pytest.fixture
def test_DeleteUser(userID):
    pass

@pytest.fixture
def test_InsertUserInfo(username, password, gender, mail, birthdate, creationdate):
    pass
    
    






