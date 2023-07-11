from app import app
import pytest

@pytest.fixture
def client(scope="session"):
    with app.test_client() as test_client:
        yield test_client

def test_app_runs_without_errors(client):
    response = client.get('/')
    assert response.status_code == 200

def test_menu(client):
    response = client.get('/menu')
    assert response.status_code == 200

def test_lunch_menu(client):
    response = client.get('/lunch')
    assert response.status_code == 200

def test_dinner_menu(client):
    response = client.get('/dinner')
    assert response.status_code == 200

def test_reservation_form(client):
    response = client.get('/reservation')
    assert response.status_code == 200

def test_reservation_submission(client):
    data = {
        'name': 'John Smith',
        'date': '2022-01-01',
        'time': '18:00',
        'party_size': '4'
    }
    response = client.post('/reservation', data=data)
    assert response.status_code == 200
