import json
import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app('testing')
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_tasks(client):
    """
    GIVEN a Flask application
    WHEN the '/tasks' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get('/tasks/')
    assert response.status_code == 200
    assert b'[]' in response.data

def test_create_task(client):
    """
    GIVEN a Flask application
    WHEN a new task is created (POST)
    THEN check the response is valid and the task is created
    """
    response = client.post('/tasks/', json={'title': 'Test task', 'description': 'Test description'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test task'
    assert data['description'] == 'Test description'