import json

from pytest_mock import MockFixture

from main import app


def test_ok(mocker: MockFixture):
    return_value = (
        [
            {
                'item_id': '1234567890',
                'name': 'iPhone 11',
                'price': '30,000',
            },
            {
                'item_id': '0987654321',
                'name': 'iPhone 12',
                'price': '40,000',
            },
        ],
        [],
    )
    mocker.patch(target='utils.momo_crawler.crawler', return_value=return_value)
    response = app.test_client().get('/items/', query_string={'keyword': 'iphone'})
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data['items'] == return_value[0]
    assert response_data['error_items'] == return_value[1]


def test_parameter_missing():
    response = app.test_client().get('/items/')
    assert response.status_code == 400


def test_partial_content(mocker: MockFixture):
    return_value = (
        [
            {
                'item_id': '1234567890',
                'name': 'iPhone 11',
                'price': '30,000',
            },
            {
                'item_id': '0987654321',
                'name': 'iPhone 12',
                'price': '40,000',
            },
        ],
        [
            {
                'item_id': '1234567890',
                'name': 'iPhone 11',
                'price': '',
            }
        ],
    )
    mocker.patch(target='utils.momo_crawler.crawler', return_value=return_value)
    response = app.test_client().get('/items/', query_string={'keyword': 'iphone'})
    response_data = json.loads(response.data)
    assert response.status_code == 206
    assert response_data['items'] == return_value[0]
    assert response_data['error_items'] == return_value[1]


def test_no_content(mocker: MockFixture):
    return_value = ([], [])

    mocker.patch(target='utils.momo_crawler.crawler', return_value=return_value)
    response = app.test_client().get('/items/', query_string={'keyword': 'iphone'})
    assert response.status_code == 204
