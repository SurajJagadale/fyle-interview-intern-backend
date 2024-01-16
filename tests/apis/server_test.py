import pytest
from flask import json
from core import app
from core.libs.exceptions import FyleError
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def client():
    return app.test_client()

def test_ready(client):
    response = client.get('/')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == 'ready'
    assert 'time' in data

def test_handle_error_FyleError(client):
    with pytest.raises(FyleError):
        raise FyleError('Test FyleError', 'This is a test message')

def test_handle_error_ValidationError(client):
    with pytest.raises(ValidationError):
        raise ValidationError('Test ValidationError')

def test_handle_error_IntegrityError(client):
    with pytest.raises(IntegrityError):
        raise IntegrityError('Test IntegrityError', None, None)

def test_handle_error_HTTPException(client):
    with pytest.raises(HTTPException):
        raise HTTPException('Test HTTPException')