import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_login_success():
    """Test standard JSON login with the seeded admin account."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/login", json={
            "email": "admin@school.com",
            "password": "password123"
        })
    
    # Assert successful login
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_failure():
    """Test login with incorrect password."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/login", json={
            "email": "admin@school.com",
            "password": "wrongpassword"
        })
    
    assert response.status_code == 400
    assert "Incorrect email or password" in response.text

@pytest.mark.asyncio
async def test_read_users_me():
    """Test fetching the current user profile with the token."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Login to get token
        login_response = await ac.post("/api/v1/auth/login", json={
            "email": "admin@school.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        # 2. Use token to get /me
        me_response = await ac.get("/api/v1/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        
    assert me_response.status_code == 200
    user_data = me_response.json()
    assert user_data["email"] == "admin@school.com"
    assert user_data["role"] == "ADMIN"
    
@pytest.mark.asyncio
async def test_read_users_me_unauthorized():
    """Test that /me is protected."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/auth/me")
    
    assert response.status_code == 401 # Unauthorized
