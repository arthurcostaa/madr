from http import HTTPStatus

from madr.schemas import UserPublic


def test_root_should_return_ok_and_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'arthur',
            'email': 'arthur@email.com',
            'password': 'password123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'arthur',
        'email': 'arthur@email.com',
    }


def test_create_user_with_email_already_used(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'anahickman',
            'email': user.email,
            'password': 'password123',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email já consta no MADR'}


def test_create_user_with_username_already_used(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'ana@test.com',
            'password': 'password123',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username já consta no MADR'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}
