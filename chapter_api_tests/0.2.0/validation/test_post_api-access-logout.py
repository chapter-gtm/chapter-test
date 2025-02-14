import os
import pytest
import httpx


@pytest.fixture
async def client():
    base_url = os.getenv('API_BASE_URL')
    async with httpx.AsyncClient(base_url=base_url) as client:
        yield client


@pytest.mark.asyncio
async def test_logout_success(client):
    response = await client.post('/api/access/logout')
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {}


@pytest.mark.asyncio
async def test_logout_unauthorized(client):
    response = await client.post('/api/access/logout', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert 'error' in response.json()


@pytest.mark.asyncio
async def test_logout_forbidden(client):
    response = await client.post('/api/access/logout', headers={'Authorization': 'Bearer forbidden_token'})
    assert response.status_code == 403
    assert response.headers['Content-Type'] == 'application/json'
    assert 'error' in response.json()


@pytest.mark.asyncio
async def test_logout_empty_response(client):
    response = await client.post('/api/access/logout')
    assert response.status_code == 201
    assert response.json() == {}


@pytest.mark.asyncio
async def test_logout_invalid_request(client):
    # Simulate a malformed request (if applicable)
    response = await client.post('/api/access/logout', json={'malformed': 'data'})
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert 'error' in response.json()


@pytest.mark.asyncio
async def test_logout_rate_limiting(client):
    # Simulate rate limiting by making multiple requests in a short time
    for _ in range(10):
        await client.post('/api/access/logout')
    response = await client.post('/api/access/logout')
    assert response.status_code == 429
    assert response.headers['Content-Type'] == 'application/json'
    assert 'error' in response.json()


@pytest.mark.asyncio
async def test_logout_server_error(client):
    # Simulate a server error (if applicable)
    response = await client.post('/api/access/logout', headers={'Authorization': 'Bearer server_error_token'})
    assert response.status_code == 500
    assert response.headers['Content-Type'] == 'application/json'
    assert 'error' in response.json()


@pytest.mark.asyncio
async def test_logout_large_payload(client):
    # Test with a large payload if applicable
    large_payload = {'data': 'x' * 10000}
    response = await client.post('/api/access/logout', json=large_payload)
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert 'error' in response.json()


@pytest.mark.asyncio
async def test_logout_empty_string(client):
    # Test with an empty string if applicable
    response = await client.post('/api/access/logout', json={'data': ''})
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert 'error' in response.json()
