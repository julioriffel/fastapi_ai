import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    response = await client.post("/api/v1/users/", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert content["email"] == data["email"]
    assert "id" in content
    assert "hashed_password" not in content

@pytest.mark.asyncio
async def test_read_users(client: AsyncClient):
    # Create a user first
    data = {
        "email": "test2@example.com",
        "password": "password123",
        "full_name": "Test User 2"
    }
    await client.post("/api/v1/users/", json=data)
    
    response = await client.get("/api/v1/users/")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) >= 1
    assert any(u["email"] == "test2@example.com" for u in content)

@pytest.mark.asyncio
async def test_read_user_me(client: AsyncClient):
    # Create user and login
    user_data = {
        "email": "me@example.com",
        "password": "password123",
        "full_name": "Me User"
    }
    await client.post("/api/v1/users/", json=user_data)
    
    login_data = {
        "username": "me@example.com",
        "password": "password123"
    }
    login_response = await client.post("/api/v1/login/access-token", data=login_data)
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["email"] == "me@example.com"
