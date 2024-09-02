from http import HTTPStatus


def test_create_book(client, novelist, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 2024,
            'title': 'New Book',
            'novelist_id': novelist.id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'year': 2024,
        'novelist_id': novelist.id,
        'title': 'new book',
    }


def test_create_book_with_unexistent_novelist(client, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 2024,
            'title': 'the best book of all time ever',
            'novelist_id': 1,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Novelist ID not found'}


def test_create_book_already_existent(client, token, novelist, book):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 2024,
            'title': book.title,
            'novelist_id': novelist.id,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Book already exists in MADR'}


def test_create_book_with_unexistent_novelist_id(client, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 2024,
            'title': 'Book',
            'novelist_id': 1,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Novelist ID not found'}


def test_delete_book(client, token, book):
    response = client.delete(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Book deleted from MADR'}


def test_delete_unexistent_book(client, token):
    response = client.delete(
        '/books/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}
