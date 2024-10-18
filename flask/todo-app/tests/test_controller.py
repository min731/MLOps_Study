import pytest
from app import create_app, db
from app.controllers.task_controller import TaskController
from app.models.task import Task

@pytest.fixture
def app():
    app = create_app('testing')
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

def test_create_task(init_database):
    """
    GIVEN a Task controller
    WHEN a new Task is created
    THEN check the title, description, and done fields are defined correctly
    """
    task_data = {'title': 'New task', 'description': 'Test description'}
    task = TaskController.create_task(task_data)
    assert task['title'] == 'New task'
    assert task['description'] == 'Test description'
    assert task['done'] == False

def test_get_all_tasks(init_database):
    """
    GIVEN a Task controller
    WHEN all tasks are requested
    THEN check if the correct number of tasks is returned
    """
    TaskController.create_task({'title': 'Task 1'})
    TaskController.create_task({'title': 'Task 2'})
    tasks = TaskController.get_all_tasks()
    assert len(tasks) == 2