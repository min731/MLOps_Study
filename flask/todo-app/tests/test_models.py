import pytest
from app.models.task import Task

def test_new_task():
    """
    GIVEN a Task model
    WHEN a new Task is created
    THEN check the title, description, and done fields are defined correctly
    """
    task = Task(title='New task', description='Test description')
    assert task.title == 'New task'
    assert task.description == 'Test description'
    assert task.done == False