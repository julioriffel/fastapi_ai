from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "up"}


@pytest.mark.asyncio
async def test_health_check_failure(client: AsyncClient) -> None:
    from unittest.mock import AsyncMock

    from app.db.session import get_session
    from app.main import app

    mock_session = AsyncMock()
    mock_session.exec.side_effect = Exception("Database connection failed")

    async def override_get_session() -> AsyncGenerator[AsyncMock, None]:
        yield mock_session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = await client.get("/api/v1/health/")
        assert response.status_code == 503
        assert response.json() == {"status": "error", "database": "down"}
    finally:
        app.dependency_overrides.clear()
