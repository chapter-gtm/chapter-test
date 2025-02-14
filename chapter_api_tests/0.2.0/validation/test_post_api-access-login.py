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
    data = response.json()
    assert 'access_token' in data
    assert 'token_type' in data


@pytest.mark.asyncio
async def test_login_missing_username():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'password': 'testpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.json()
    assert data['status_code'] == 400
    assert data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_missing_password():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'testuser'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.json()
    assert data['status_code'] == 400
    assert data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_empty_username():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': '', 'password': 'testpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.json()
    assert data['status_code'] == 400
    assert data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_empty_password():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'testuser', 'password': ''}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.json()
    assert data['status_code'] == 400
    assert data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'invaliduser', 'password': 'wrongpass'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.json()
    assert data['status_code'] == 400
    assert data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_large_payload():
    url = f'{API_BASE_URL}/api/access/login'
    payload = {'username': 'testuser', 'password': 'testpass', 'extra_field': 'x' * 10000}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.json()
    assert data['status_code'] == 400
    assert data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_unauthorized():
    url = f'{API_BASE_URL}/api/access/login'
    response = await httpx.post(url, json={})  # No credentials

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.json()
    assert data['status_code'] == 400
    assert data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_invalid_json():
    url = f'{API_BASE_URL}/api/access/login'
    response = await httpx.post(url, data='invalid_json')

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.json()
    assert data['status_code'] == 400
    assert data['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_login_server_error():
    url = f'{API_BASE_URL}/api/access/login'
    # Simulate server error by sending a request that triggers it
    payload = {'username': 'testuser', 'password': 'trigger_error'}
    response = await httpx.post(url, json=payload)

    assert response.status_code == 500  # Assuming this triggers a server error
    assert response.headers['Content-Type'] == 'application/json'

