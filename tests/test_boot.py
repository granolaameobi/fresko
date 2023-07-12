from app import app
import pytest
import datetime

today = datetime.date.today()
current_date = today.strftime('%d-%m-%Y')

request = {
        'first_name': 'Joe',
        'last_name': 'Bloggs',
        'email':'joe.bloggs@example.com',
        'contact_number':'+441111111111',
        'date': current_date,
        'time': '18:00',
        'party_size': '4'
    }
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

def test_nutrition(client):
    response = client.get('/nutrition')
    assert response.status_code == 200

def test_delivery(client):
    response = client.get('/delivery')
    assert response.status_code == 200

def test_reservation_submission(client):
    response = client.post('/reservation', data=request)
    assert response.status_code == 200
