import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_login_access_token(client: AsyncClient):
    # Create user first
    user_data = {
        "email": "login@example.com",
        "password": "password123",
        "full_name": "Login User"
    }
    await client.post("/api/v1/users/", json=user_data)
    
    # Try to login
    login_data = {
        "username": "login@example.com",
        "password": "password123"
    }
    response = await client.post("/api/v1/login/access-token", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_access_token_incorrect_password(client: AsyncClient):
    # Create user first
    user_data = {
        "email": "wrongpass@example.com",
        "password": "password123",
        "full_name": "Login User"
    }
    await client.post("/api/v1/users/", json=user_data)
    
    # Try to login with wrong password
    login_data = {
        "username": "wrongpass@example.com",
        "password": "wrongpassword"
    }
    response = await client.post("/api/v1/login/access-token", data=login_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Incorrect email or password"
