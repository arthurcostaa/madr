from http import HTTPStatus

from tests.conftest import NovelistFactory


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


def test_read_unexistent_novelist(session, client, token):
    response = client.get(
        '/novelists/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Novelist not found in MADR'}


def test_read_novelists_should_return_5_novelists(session, client, token):
    expected_novelists = 5
    session.bulk_save_objects(NovelistFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/novelists/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['novelists']) == expected_novelists


def test_read_novelists_with_negative_offset(client, token):
    response = client.get(
        '/novelists/?offset=-1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Offset must be a non-negative integer'
    }


def test_read_novelists_with_negative_limit(client, token):
    response = client.get(
        '/novelists/?limit=-1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Limit must be a non-negative integer'
    }


def test_read_novelists_pagination_should_return_3_novelists(
    session, client, token
):
    expected_novelists = 3
    session.bulk_save_objects(NovelistFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/novelists/?offset=1&limit=3',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['novelists']) == expected_novelists


def test_read_novelists_filter_name_should_return_5_novelists(
    session, client, token
):
    expected_novelists = 5
    session.bulk_save_objects(NovelistFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/novelists/?name=novelist',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['novelists']) == expected_novelists


def test_read_novelists_should_return_empty_list(client, token):
    response = client.get(
        '/novelists/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response.json()['novelists'] == {'novelists': []}
