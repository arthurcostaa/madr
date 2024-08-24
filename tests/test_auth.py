from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert token['access_token']


def test_get_token_with_unused_email(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'email@email.com', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_with_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'asdf123'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
