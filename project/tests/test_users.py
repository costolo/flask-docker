# project/tests/test_users.py

import json
from project.api.models import User


# POST tests
def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'beb',
            'email': 'beb@lol.io'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'beb@lol.io was added!' in data['message']


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({"email": "beb@lol.io"}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/users',
        data=json.dumps({
            "username": "beb",
            "email": "beb@lol.io"
        }),
        content_type='application/json',
    )
    resp = client.post(
        '/users',
        data=json.dumps({
            "username": "beb",
            "email": "beb@lol.io"
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry. That email already exists.' in data['message']


# GET tests
def test_single_user(test_app, test_database, add_user):
    user = add_user(username='beb', email='beb@lol.io')
    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'beb' in data['username']
    assert 'beb@lol.io' in data['email']


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/users/9999')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'User 9999 does not exist' in data['message']


def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user(email='lol@test.io', username='lol')
    add_user(email='lol2@test.io', username='lol2')
    client = test_app.test_client()
    resp = client.get('/users')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert 'lol@test.io' in data[0]['email']
    assert 'lol' in data[0]['username']
    assert 'lol2@test.io' in data[1]['email']
    assert 'lol2' in data[1]['username']
