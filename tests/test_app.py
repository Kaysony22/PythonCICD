import pytest
from flask import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_todos(client):
    rv = client.get('/todos')
    assert rv.status_code == 200
    assert json.loads(rv.data) == []

def test_add_todo_success(client):
    rv = client.post('/todos', json={'todo': 'Test Todo'})
    assert rv.status_code == 201
    assert json.loads(rv.data) == {'message': 'Todo added successfully!'}

    rv = client.get('/todos')
    assert rv.status_code == 200
    assert json.loads(rv.data) == ['Test Todo']

def test_add_todo_failure(client):
    rv = client.post('/todos', json={})
    assert rv.status_code == 400
    assert json.loads(rv.data) == {'message': 'Todo is required!'}

def test_delete_todo_success(client):
    client.post('/todos', json={'todo': 'Test Todo'})
    rv = client.delete('/todos/0')
    assert rv.status_code == 200
    assert json.loads(rv.data) == {'message': 'Todo deleted successfully!'}

    rv = client.get('/todos')
    assert rv.status_code == 200
    assert json.loads(rv.data) == []

def test_delete_todo_failure(client):
    rv = client.delete('/todos/0')
    assert rv.status_code == 404
    assert json.loads(rv.data) == {'message': 'Todo not found!'}