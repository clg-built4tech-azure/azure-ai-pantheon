# Basic tests for the MAF orchestrator (Phase 1)

import pytest
import asyncio
from httpx import AsyncClient

# Note: These tests assume the app is importable and mocks are running
# For full integration tests, use docker compose and test against ports

from app.main import app
from app.workflows.task_router import run_simple_workflow

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_simple_workflow():
    result = await run_simple_workflow("Analyze this complex problem")
    assert "plan" in result
    assert "results" in result
    assert len(result["results"]) > 0

@pytest.mark.asyncio
async def test_orchestrate_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/orchestrate", json={"prompt": "Execute a simple task"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "processed"
        assert "result" in data
