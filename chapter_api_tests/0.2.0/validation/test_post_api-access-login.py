import os
import pytest
import httpx

API_BASE_URL = os.getenv('API_BASE_URL')


@pytest.mark.asyncio
async def test_login_success():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'testuser', 'password': 'testpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    response_data = response.json()
    assert 'access_token' in response_data
    assert 'token_type' in response_data


@pytest.mark.asyncio
async def test_login_missing_username():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'password': 'testpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status_code'] == 400
    assert response_data['detail'] == 'Bad Request'
    assert 'extra' in response_data


@pytest.mark.asyncio
async def test_login_missing_password():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'testuser'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status_code'] == 400
    assert response_data['detail'] == 'Bad Request'
    assert 'extra' in response_data


@pytest.mark.asyncio
async def test_login_invalid_username_type():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 12345, 'password': 'testpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status_code'] == 400
    assert response_data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_empty_payload():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status_code'] == 400
    assert response_data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_unauthorized():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'invaliduser', 'password': 'wrongpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_large_payload():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'testuser', 'password': 'testpass' * 1000}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status_code'] == 400
    assert response_data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_forbidden():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'forbiddenuser', 'password': 'forbiddenpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_login_malformed_request():
    url = f'{API_BASE_URL}/api/access/login'
    response = await httpx.post(url, data='malformed data')

    assert response.status_code == 400
    response_data = response.json()
    assert response_data['status_code'] == 400
    assert response_data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_server_error():
    url = f'{API_BASE_URL}/api/access/login'
    # Simulate server error by hitting an invalid endpoint
    response = await httpx.post(url + '/invalid')

    assert response.status_code == 500
