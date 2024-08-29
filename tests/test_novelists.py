from http import HTTPStatus


def test_create_novelist(client, token):
    response = client.post(
        '/novelists/',
        json={'name': 'Clarice Lispector'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'clarice lispector'}


def test_create_existent_novelist(client, token, novelist):
    response = client.post(
        '/novelists/',
        json={'name': novelist.name},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Novelist already exists.'}


def test_delete_novelist(client, novelist, token):
    response = client.delete(
        f'/novelists/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Novelist deleted from MADR'}


def test_delete_unexistent_novelist(client, novelist, token):
    response = client.delete(
        f'/novelists/{novelist.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Novelist not found in MADR'}
