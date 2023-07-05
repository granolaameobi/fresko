from app import app
import pytest

def test_app_runs_without_errors():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
