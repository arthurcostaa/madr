from http import HTTPStatus

from madr.schemas import UserPublic


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


def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'ana',
            'email': 'ana@test.com',
            'password': 'password123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'ana',
        'email': 'ana@test.com',
    }


def test_update_user_with_wrong_id(client, user):
    response = client.put(
        f'/users/{user.id + 1}',
        json={
            'username': user.username,
            'email': user.email,
            'password': '12345',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não consta no MADR'}


def test_update_user_with_username_already_used(client, user, other_user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': other_user.username,
            'email': user.email,
            'password': '12345',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username já consta no MADR'}


def test_update_user_with_email_already_used(client, user, other_user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': user.username,
            'email': other_user.email,
            'password': '12345',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email já consta no MADR'}


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_delete_user_with_wrong_user(client, user):
    response = client.delete(f'/users/{user.id + 1}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não consta no MADR'}
