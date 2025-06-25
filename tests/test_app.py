from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # client = TestClient(app)  # Arrange (organização)

    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {'message': 'Olá Mundo!'}


def test_exercicio_ola_mundo_em_html(client):
    # client = TestClient(app)

    response = client.get('/exercicio-html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text


# def test_get_user_should_return_not_found__exercicio(client):
#     response = client.get('/users/666')
#
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


# def test_get_user___exercicio(client):
#     response = client.get('/users/1')
#
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {
#         'username': 'bob',
#         'email': 'bob@example.com',
#         'id': 1,
#     }
