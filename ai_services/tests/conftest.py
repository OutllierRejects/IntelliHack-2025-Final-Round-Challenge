import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_supabase():
    """Mock Supabase client for testing"""
    with patch("supabase.create_client") as mock:
        mock_client = Mock()
        mock_client.table.return_value.select.return_value.execute.return_value.data = (
            []
        )
        mock.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_openai():
    """Mock OpenAI client for testing agents"""
    with patch("openai.OpenAI") as mock:
        mock_client = Mock()
        mock_client.chat.completions.create.return_value.choices = [
            Mock(message=Mock(content="Test response"))
        ]
        mock.return_value = mock_client
        yield mock_client


@pytest.fixture
def test_client():
    """FastAPI test client"""
    from main import app

    return TestClient(app)


@pytest.fixture
def test_env():
    """Set up test environment variables"""
    os.environ.update(
        {
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_ANON_KEY": "test-anon-key",
            "SUPABASE_SERVICE_ROLE_KEY": "test-service-key",
            "OPENAI_API_KEY": "test-openai-key",
            "JWT_SECRET": "test-jwt-secret",
            "DEBUG": "true",
            "ENVIRONMENT": "test",
        }
    )
    yield
    # Cleanup would go here if needed
