# Testing Guide

This document provides comprehensive guidance for testing the disaster response coordination web application.

## Testing Philosophy

Our testing strategy follows the testing pyramid approach:
- **Unit Tests**: Fast, isolated tests for individual functions and components
- **Integration Tests**: Tests for interactions between components
- **End-to-End Tests**: Full workflow tests simulating real user scenarios

## Testing Stack

### Frontend Testing
- **Jest**: JavaScript testing framework
- **React Testing Library**: React component testing utilities
- **MSW (Mock Service Worker)**: API mocking for tests
- **Cypress**: End-to-end testing framework

### Backend Testing
- **pytest**: Python testing framework
- **pytest-asyncio**: Async test support
- **httpx**: Async HTTP client for API testing
- **SQLAlchemy Testing**: Database testing utilities

### AI Services Testing
- **pytest**: Python testing framework
- **unittest.mock**: Mocking for AI model calls
- **MCP Testing**: Custom testing utilities for MCP tools

## Running Tests

### Frontend Tests

```bash
# Navigate to frontend directory
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run specific test file
npm test -- UserDashboard.test.tsx

# Run E2E tests
npm run test:e2e
```

### Backend Tests

```bash
# Navigate to backend directory
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run tests with verbose output
pytest -v

# Run integration tests only
pytest tests/integration/
```

### AI Services Tests

```bash
# Navigate to AI services directory
cd ai_services

# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=mcp_integration

# Run specific test module
pytest tests/test_emergency_agent.py
```

## Test Structure

### Frontend Test Organization

```
frontend/src/
├── components/
│   ├── __tests__/           # Component tests
│   │   ├── Dashboard.test.tsx
│   │   ├── RequestForm.test.tsx
│   │   └── UserProfile.test.tsx
│   └── ...
├── services/
│   ├── __tests__/           # Service tests
│   │   ├── api.test.ts
│   │   └── websocket.test.ts
│   └── ...
├── utils/
│   ├── __tests__/           # Utility tests
│   │   └── helpers.test.ts
│   └── ...
└── __tests__/               # Integration tests
    ├── App.test.tsx
    └── routing.test.tsx
```

### Backend Test Organization

```
backend/tests/
├── unit/                    # Unit tests
│   ├── api/
│   │   ├── test_auth.py
│   │   ├── test_requests.py
│   │   └── test_tasks.py
│   ├── services/
│   │   ├── test_auth_service.py
│   │   └── test_request_service.py
│   └── models/
│       ├── test_user.py
│       └── test_request.py
├── integration/             # Integration tests
│   ├── test_api_integration.py
│   ├── test_websocket_integration.py
│   └── test_database_integration.py
├── e2e/                     # End-to-end tests
│   ├── test_emergency_workflow.py
│   └── test_volunteer_workflow.py
├── fixtures/                # Test data and fixtures
│   ├── users.py
│   ├── requests.py
│   └── tasks.py
└── conftest.py             # Pytest configuration
```

## Writing Tests

### Frontend Component Tests

```typescript
// components/__tests__/EmergencyRequestForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { EmergencyRequestForm } from '../EmergencyRequestForm';

describe('EmergencyRequestForm', () => {
  it('should submit emergency request with valid data', async () => {
    const mockSubmit = jest.fn();
    render(<EmergencyRequestForm onSubmit={mockSubmit} />);
    
    // Fill form fields
    fireEvent.change(screen.getByLabelText(/emergency type/i), {
      target: { value: 'medical' }
    });
    
    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: 'Medical emergency at location' }
    });
    
    // Submit form
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        type: 'medical',
        description: 'Medical emergency at location'
      });
    });
  });
  
  it('should display validation errors for invalid input', async () => {
    render(<EmergencyRequestForm onSubmit={jest.fn()} />);
    
    // Submit without filling required fields
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/emergency type is required/i)).toBeInTheDocument();
    });
  });
});
```

### Backend API Tests

```python
# tests/unit/api/test_requests.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_emergency_request():
    """Test creating a new emergency request."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        request_data = {
            "type": "medical",
            "description": "Medical emergency",
            "location": {
                "latitude": 40.7128,
                "longitude": -74.0060
            },
            "priority": "high"
        }
        
        response = await client.post("/api/v1/requests", json=request_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "medical"
        assert data["status"] == "pending"
        assert "id" in data

@pytest.mark.asyncio
async def test_get_requests_requires_authentication():
    """Test that getting requests requires authentication."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/requests")
        assert response.status_code == 401
```

### AI Agent Tests

```python
# tests/unit/agents/test_emergency_agent.py
import pytest
from unittest.mock import Mock, patch
from ai_services.agents.emergency_agent import EmergencyAgent

@pytest.fixture
def emergency_agent():
    return EmergencyAgent()

@pytest.mark.asyncio
async def test_process_emergency_request(emergency_agent):
    """Test emergency request processing."""
    request_data = {
        "type": "fire",
        "description": "Building fire on Main Street",
        "location": {"latitude": 40.7128, "longitude": -74.0060},
        "priority": "critical"
    }
    
    with patch.object(emergency_agent, '_analyze_severity') as mock_analyze:
        mock_analyze.return_value = {"severity": 9, "resources_needed": ["fire_truck", "ambulance"]}
        
        result = await emergency_agent.process_request(request_data)
        
        assert result["priority"] == "critical"
        assert "fire_truck" in result["resources_needed"]
        mock_analyze.assert_called_once()

@pytest.mark.asyncio
async def test_resource_allocation(emergency_agent):
    """Test resource allocation logic."""
    available_resources = [
        {"id": 1, "type": "fire_truck", "location": {"lat": 40.7130, "lng": -74.0055}},
        {"id": 2, "type": "ambulance", "location": {"lat": 40.7125, "lng": -74.0065}}
    ]
    
    request_location = {"latitude": 40.7128, "longitude": -74.0060}
    
    allocation = await emergency_agent.allocate_resources(
        available_resources, 
        request_location, 
        ["fire_truck", "ambulance"]
    )
    
    assert len(allocation) == 2
    assert allocation[0]["type"] in ["fire_truck", "ambulance"]
```

## Test Data Management

### Database Test Setup

```python
# tests/conftest.py
import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_db():
    """Create test database."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
async def db_session(test_db):
    """Create database session for tests."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
```

### Test Fixtures

```python
# tests/fixtures/users.py
import pytest
from app.models.user import User

@pytest.fixture
def sample_user():
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "role": "volunteer"
    }

@pytest.fixture
def first_responder_user():
    return {
        "email": "responder@emergency.gov",
        "password": "securepassword123",
        "full_name": "Emergency Responder",
        "role": "first_responder",
        "organization": "City Emergency Services"
    }
```

## Mocking and Stubbing

### API Mocking with MSW

```typescript
// src/__tests__/mocks/handlers.ts
import { rest } from 'msw';

export const handlers = [
  // Mock authentication
  rest.post('/api/v1/auth/login', (req, res, ctx) => {
    return res(
      ctx.json({
        access_token: 'mock-token',
        token_type: 'bearer',
        user: {
          id: 1,
          email: 'test@example.com',
          role: 'volunteer'
        }
      })
    );
  }),
  
  // Mock emergency requests
  rest.get('/api/v1/requests', (req, res, ctx) => {
    return res(
      ctx.json([
        {
          id: 1,
          type: 'medical',
          description: 'Medical emergency',
          status: 'pending',
          priority: 'high'
        }
      ])
    );
  })
];
```

### AI Model Mocking

```python
# tests/mocks/ai_mocks.py
from unittest.mock import Mock

def mock_llm_response():
    """Mock language model response."""
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content='{"priority": "high", "resources": ["ambulance"]}'))
    ]
    return mock_response

def mock_embedding_response():
    """Mock embedding model response."""
    return [0.1, 0.2, 0.3, 0.4, 0.5] * 200  # 1000-dimensional vector
```

## End-to-End Testing

### Cypress E2E Tests

```typescript
// cypress/e2e/emergency-workflow.cy.ts
describe('Emergency Request Workflow', () => {
  beforeEach(() => {
    // Login as affected individual
    cy.login('affected@example.com', 'password');
  });
  
  it('should complete full emergency request workflow', () => {
    // Submit emergency request
    cy.visit('/emergency-request');
    cy.get('[data-cy=emergency-type]').select('medical');
    cy.get('[data-cy=description]').type('Chest pain and difficulty breathing');
    cy.get('[data-cy=location-button]').click();
    cy.get('[data-cy=submit-request]').click();
    
    // Verify request was created
    cy.get('[data-cy=request-confirmation]').should('be.visible');
    cy.get('[data-cy=request-id]').should('contain', 'REQ-');
    
    // Check request status
    cy.visit('/my-requests');
    cy.get('[data-cy=request-list]').should('contain', 'medical');
    cy.get('[data-cy=request-status]').should('contain', 'pending');
  });
});
```

### Backend E2E Tests

```python
# tests/e2e/test_emergency_workflow.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_complete_emergency_workflow():
    """Test complete emergency response workflow."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 1. User registers
        user_data = {
            "email": "emergency@test.com",
            "password": "testpass123",
            "full_name": "Emergency User",
            "role": "affected_individual"
        }
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        
        # 2. User logs in
        login_data = {"email": "emergency@test.com", "password": "testpass123"}
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. User submits emergency request
        request_data = {
            "type": "medical",
            "description": "Medical emergency",
            "location": {"latitude": 40.7128, "longitude": -74.0060},
            "priority": "high"
        }
        response = await client.post("/api/v1/requests", json=request_data, headers=headers)
        assert response.status_code == 201
        request_id = response.json()["id"]
        
        # 4. Check request status
        response = await client.get(f"/api/v1/requests/{request_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["status"] == "pending"
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci
      - name: Run tests
        working-directory: ./frontend
        run: npm test -- --coverage --watchAll=false
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        working-directory: ./backend
        run: |
          pip install -r requirements.txt
          pip install pytest-cov
      - name: Run tests
        working-directory: ./backend
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Test Best Practices

1. **Test Naming**: Use descriptive names that explain what is being tested
2. **Test Organization**: Group related tests and use consistent structure
3. **Test Data**: Use fixtures and factories for consistent test data
4. **Mocking**: Mock external dependencies and services
5. **Coverage**: Aim for high test coverage but focus on critical paths
6. **Performance**: Keep tests fast and independent
7. **Maintenance**: Keep tests updated with code changes

## Debugging Tests

### Frontend Test Debugging

```bash
# Run tests in debug mode
npm test -- --detectOpenHandles --verbose

# Run single test file in debug mode
npm test -- --testNamePattern="should submit emergency request" --verbose
```

### Backend Test Debugging

```bash
# Run tests with detailed output
pytest -v -s

# Run specific test with debugging
pytest tests/test_auth.py::test_login -v -s --pdb
```

This comprehensive testing guide ensures the reliability and quality of the disaster response coordination system across all components.
