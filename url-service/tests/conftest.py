import pytest
import os
import time
from flask_jwt_extended import create_access_token
from app import create_app
from app.extensions.database import db

db_path = "./instance/test.db"

class UserData:
    id = "f0e7d012-df2f-4d17-8483-b22a6845cce6"
    username = "testuser"
    password = "testpassword"
    email = "testuser@example.com"
    role = "member"
    access_token = None
    url_key = "xyz"
    redirect_url = "https://github.com"

class AdminUserData:
    id = "18159319-08e4-478b-9ff6-eecf4bb44ed8"
    username = "testadmin"
    password = "testpassword"
    email = "testuser@example.com"
    role = "admin"
    access_token = None
    url_key = "xyz"
    redirect_url = "https://admin.example.org"

@pytest.fixture(scope="session")
def app():
    _app = create_app()

    with _app.app_context():
        yield _app
        db.session.remove()
        db.engine.dispose()
        if os.path.exists(db_path):
            os.remove(db_path)

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture(scope="session")
def headers():
    access_token = create_access_token(identity=UserData.id, additional_claims={"role": UserData.role})

    return {
        "Authorization": f"Bearer {access_token}"
    }

@pytest.fixture(scope="session")
def admin_headers():
    access_token = create_access_token(identity=AdminUserData.id, additional_claims={"role": AdminUserData.role})

    return {
        "Authorization": f"Bearer {access_token}"
    }