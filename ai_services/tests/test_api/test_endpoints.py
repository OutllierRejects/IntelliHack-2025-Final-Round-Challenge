"""
API endpoint tests for the Disaster Response Coordination App
"""

import pytest
from fastapi.testclient import TestClient
import json


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_health_check(self, test_client):
        """Test the main health check endpoint"""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_agents_health(self, test_client):
        """Test agent health status"""
        response = test_client.get("/agents/status")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data


class TestIncidentEndpoints:
    """Test incident management endpoints"""

    def test_create_incident(self, test_client, mock_supabase):
        """Test creating a new incident"""
        incident_data = {
            "title": "Test Fire Emergency",
            "description": "Test fire in downtown area",
            "location": "123 Main St",
            "incident_type": "FIRE",
            "severity": "HIGH",
            "status": "ACTIVE",
            "reporter_contact": "test@example.com",
        }

        # Mock successful database insertion
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
            {**incident_data, "id": 1, "created_at": "2024-01-01T00:00:00Z"}
        ]

        response = test_client.post("/api/incidents", json=incident_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == incident_data["title"]
        assert "id" in data

    def test_get_incidents(self, test_client, mock_supabase):
        """Test retrieving incidents"""
        mock_incidents = [
            {
                "id": 1,
                "title": "Fire Emergency",
                "status": "ACTIVE",
                "created_at": "2024-01-01T00:00:00Z",
            },
            {
                "id": 2,
                "title": "Flood Warning",
                "status": "RESOLVED",
                "created_at": "2024-01-01T01:00:00Z",
            },
        ]

        mock_supabase.table.return_value.select.return_value.execute.return_value.data = (
            mock_incidents
        )

        response = test_client.get("/api/incidents")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Fire Emergency"

    def test_get_incident_by_id(self, test_client, mock_supabase):
        """Test retrieving a specific incident"""
        mock_incident = {
            "id": 1,
            "title": "Fire Emergency",
            "description": "Building fire downtown",
            "status": "ACTIVE",
        }

        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            mock_incident
        ]

        response = test_client.get("/api/incidents/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Fire Emergency"

    def test_update_incident_status(self, test_client, mock_supabase):
        """Test updating incident status"""
        update_data = {"status": "RESOLVED"}

        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [
            {"id": 1, "status": "RESOLVED"}
        ]

        response = test_client.patch("/api/incidents/1/status", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "RESOLVED"


class TestResourceEndpoints:
    """Test resource management endpoints"""

    def test_get_resources(self, test_client, mock_supabase):
        """Test retrieving available resources"""
        mock_resources = [
            {
                "id": 1,
                "name": "Fire Truck #1",
                "type": "FIRE_TRUCK",
                "status": "AVAILABLE",
                "location": "Station A",
            },
            {
                "id": 2,
                "name": "Ambulance #1",
                "type": "AMBULANCE",
                "status": "BUSY",
                "location": "Hospital",
            },
        ]

        mock_supabase.table.return_value.select.return_value.execute.return_value.data = (
            mock_resources
        )

        response = test_client.get("/api/resources")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Fire Truck #1"

    def test_assign_resource(self, test_client, mock_supabase):
        """Test assigning a resource to an incident"""
        assignment_data = {
            "resource_id": 1,
            "incident_id": 1,
            "assigned_by": "admin@example.com",
        }

        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
            {**assignment_data, "id": 1, "assigned_at": "2024-01-01T00:00:00Z"}
        ]

        response = test_client.post("/api/resources/assign", json=assignment_data)
        assert response.status_code == 201
        data = response.json()
        assert data["resource_id"] == 1
        assert data["incident_id"] == 1


class TestUserEndpoints:
    """Test user management endpoints"""

    def test_user_registration(self, test_client, mock_supabase):
        """Test user registration"""
        user_data = {
            "email": "newuser@example.com",
            "password": "securepassword123",
            "full_name": "New User",
            "role": "VOLUNTEER",
            "phone": "+1234567890",
        }

        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
            {**user_data, "id": 1, "created_at": "2024-01-01T00:00:00Z"}
        ]

        response = test_client.post("/api/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert "password" not in data  # Password should not be returned

    def test_user_login(self, test_client, mock_supabase):
        """Test user login"""
        login_data = {"email": "user@example.com", "password": "password123"}

        # Mock user exists in database
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {
                "id": 1,
                "email": "user@example.com",
                "hashed_password": "$2b$12$hashedpassword",
                "role": "VOLUNTEER",
            }
        ]

        with pytest.MonkeyPatch().context() as mp:
            # Mock password verification
            mp.setattr("services.auth_service.verify_password", lambda x, y: True)
            mp.setattr(
                "services.auth_service.create_access_token", lambda x: "mock_jwt_token"
            )

            response = test_client.post("/api/auth/login", json=login_data)
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"


class TestAgentEndpoints:
    """Test agent management endpoints"""

    def test_trigger_agent_processing(self, test_client, mock_openai):
        """Test triggering agent processing"""
        response = test_client.post("/api/agents/process")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["status"] == "processing"

    def test_get_agent_status(self, test_client):
        """Test getting agent status"""
        response = test_client.get("/api/agents/status")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert isinstance(data["agents"], dict)


class TestWebSocketEndpoints:
    """Test WebSocket connections"""

    def test_websocket_connection(self, test_client):
        """Test WebSocket connection establishment"""
        with test_client.websocket_connect("/ws") as websocket:
            # Test connection established
            data = websocket.receive_json()
            assert data["type"] == "connection_established"

    def test_websocket_notifications(self, test_client):
        """Test receiving notifications via WebSocket"""
        with test_client.websocket_connect("/ws") as websocket:
            # Mock sending a notification
            websocket.send_json({"type": "subscribe", "channel": "incidents"})

            # Should receive subscription confirmation
            data = websocket.receive_json()
            assert data["type"] == "subscription_confirmed"
