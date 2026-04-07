import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_redirect_to_docs(client: AsyncClient) -> None:
    """Test that the root endpoint redirects to /docs"""
    response = await client.get("/", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "/docs"
