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


def test_update_novelist(client, novelist, token):
    response = client.patch(
        f'/novelists/{novelist.id}',
        json={'name': 'Arthur Conan Doyle'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': novelist.id, 'name': 'arthur conan doyle'}


def test_update_unexistent_novelist(client, novelist, token):
    response = client.patch(
        f'/novelists/{novelist.id + 1}',
        json={'name': 'Arthur Conan Doyle'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Novelist not found in MADR'}


def test_update_novelist_with_name_already_used(
    client, novelist, other_novelist, token
):
    response = client.patch(
        f'/novelists/{novelist.id}',
        json={'name': other_novelist.name},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Novelist already exists in MADR'}


def test_read_novelist(client, novelist, token):
    response = client.get(
        f'/novelists/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': novelist.id, 'name': novelist.name}


def test_read_unexistent_novelist(client, token):
    response = client.get(
        '/novelists/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Novelist not found in MADR'}
