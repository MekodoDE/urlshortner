import pytest
import os
from app import create_app

db_path = "./instance/test2.db"

class UserData:
    id = None
    username = "testuser"
    password = "testpassword"
    email = "testuser@example.com"
    access_token = None


@pytest.fixture(scope='session')
def app():
    _app = create_app()
    yield _app
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def headers(client):
    return {
        'Authorization': f'Bearer {UserData.access_token}'
    }