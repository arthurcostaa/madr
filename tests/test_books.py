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


def test_patch_book(client, token, book, other_novelist):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 2024,
            'title': 'New book',
            'novelist_id': other_novelist.id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'year': 2024,
        'title': 'new book',
        'novelist_id': other_novelist.id,
    }


def test_patch_unexistent_book(client, token, novelist):
    response = client.patch(
        '/books/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 2024,
            'title': 'New book',
            'novelist_id': novelist.id,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}


def test_patch_book_with_name_already_used(
    client, token, book, other_book, novelist
):
    response = client.patch(
        f'/books/{other_book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 2024,
            'title': book.title,
            'novelist_id': novelist.id,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Book already exists in MADR'}


def test_read_book(client, token, book):
    response = client.get(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'novelist_id': book.novelist_id,
        'title': book.title,
        'year': book.year,
    }


def test_read_unexistent_book(client, token):
    response = client.get(
        '/books/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}
