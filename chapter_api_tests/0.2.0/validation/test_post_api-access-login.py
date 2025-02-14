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
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


@pytest.mark.asyncio
async def test_login_missing_username():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'password': 'testpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.json()['status_code'] == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_missing_password():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'testuser'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.json()['status_code'] == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_empty_username():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': '', 'password': 'testpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.json()['status_code'] == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_empty_password():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'testuser', 'password': ''}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.json()['status_code'] == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'invaliduser', 'password': 'wrongpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.json()['status_code'] == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_large_payload():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'testuser', 'password': 'testpass' * 1000}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.json()['status_code'] == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_unauthorized():
    url = f'{API_BASE_URL}/api/access/login'
    # Assuming the API requires a token for some reason
    headers = {'Authorization': 'Bearer invalid_token'}
    payload = {'username': 'testuser', 'password': 'testpass'}
    response = await httpx.post(url, json=payload, headers=headers)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_forbidden():
    url = f'{API_BASE_URL}/api/access/login'
    # Assuming the API has some role-based access
    headers = {'Authorization': 'Bearer forbidden_token'}
    payload = {'username': 'testuser', 'password': 'testpass'}
    response = await httpx.post(url, json=payload, headers=headers)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_login_malformed_request():
    url = f'{API_BASE_URL}/api/access/login'
    response = await httpx.post(url, data='malformed_data')

    assert response.status_code == 400
    assert response.json()['status_code'] == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_server_error():
    url = f'{API_BASE_URL}/api/access/login'
    # Simulate a server error by sending a request that triggers it
    payload = {'username': 'testuser', 'password': 'testpass'}
    response = await httpx.post(url, json=payload)

    # Assuming the server is down or there's an internal error
    assert response.status_code == 500
