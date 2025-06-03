"""
Service layer tests for the Disaster Response Coordination App
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone

from services.notification_service import NotificationService
from services.auth_service import AuthService
from services.incident_service import IncidentService

class TestNotificationService:
    """Test notification service functionality"""
    
    @pytest.fixture
    def notification_service(self):
        """Create notification service instance"""
        return NotificationService()
    
    @pytest.mark.asyncio
    async def test_send_email_notification(self, notification_service):
        """Test sending email notifications"""
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = Mock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            result = await notification_service.send_email(
                to_email="test@example.com",
                subject="Test Emergency Alert",
                body="This is a test emergency notification"
            )
            
            assert result == True
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once()
            mock_server.send_message.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_sms_notification(self, notification_service):
        """Test sending SMS notifications"""
        with patch('twilio.rest.Client') as mock_twilio:
            mock_client = Mock()
            mock_twilio.return_value = mock_client
            mock_client.messages.create.return_value = Mock(sid="test_sid")
            
            result = await notification_service.send_sms(
                to_phone="+1234567890",
                message="Emergency alert: Fire reported in your area"
            )
            
            assert result == True
            mock_client.messages.create.assert_called_once()
    
    def test_format_notification_template(self, notification_service):
        """Test notification template formatting"""
        template = "Emergency at {location}. Status: {status}. Contact: {contact}"
        data = {
            "location": "Downtown",
            "status": "ACTIVE", 
            "contact": "911"
        }
        
        result = notification_service.format_template(template, data)
        expected = "Emergency at Downtown. Status: ACTIVE. Contact: 911"
        assert result == expected

class TestAuthService:
    """Test authentication service functionality"""
    
    @pytest.fixture
    def auth_service(self):
        """Create auth service instance"""
        return AuthService()
    
    def test_password_hashing(self, auth_service):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = auth_service.hash_password(password)
        
        assert hashed != password
        assert auth_service.verify_password(password, hashed) == True
        assert auth_service.verify_password("wrongpassword", hashed) == False
    
    def test_jwt_token_creation(self, auth_service):
        """Test JWT token creation and validation"""
        user_data = {"sub": "user@example.com", "role": "VOLUNTEER"}
        token = auth_service.create_access_token(user_data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Test token validation
        decoded = auth_service.decode_token(token)
        assert decoded["sub"] == "user@example.com"
        assert decoded["role"] == "VOLUNTEER"
    
    def test_invalid_token_handling(self, auth_service):
        """Test handling of invalid tokens"""
        with pytest.raises(Exception):
            auth_service.decode_token("invalid.token.here")

class TestIncidentService:
    """Test incident service functionality"""
    
    @pytest.fixture
    def incident_service(self, mock_supabase):
        """Create incident service instance"""
        return IncidentService()
    
    @pytest.mark.asyncio
    async def test_create_incident(self, incident_service, mock_supabase):
        """Test incident creation"""
        incident_data = {
            "title": "Test Emergency",
            "description": "Test description",
            "location": "Test Location",
            "incident_type": "FIRE",
            "severity": "HIGH"
        }
        
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
            {**incident_data, "id": 1, "created_at": "2024-01-01T00:00:00Z"}
        ]
        
        result = await incident_service.create_incident(incident_data)
        
        assert result["id"] == 1
        assert result["title"] == "Test Emergency"
        assert result["status"] == "ACTIVE"  # Default status
    
    @pytest.mark.asyncio
    async def test_get_incidents_by_status(self, incident_service, mock_supabase):
        """Test retrieving incidents by status"""
        mock_incidents = [
            {"id": 1, "title": "Active Fire", "status": "ACTIVE"},
            {"id": 2, "title": "Active Flood", "status": "ACTIVE"}
        ]
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = mock_incidents
        
        result = await incident_service.get_incidents_by_status("ACTIVE")
        
        assert len(result) == 2
        assert all(incident["status"] == "ACTIVE" for incident in result)
    
    @pytest.mark.asyncio
    async def test_update_incident_status(self, incident_service, mock_supabase):
        """Test updating incident status"""
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [
            {"id": 1, "status": "RESOLVED", "resolved_at": "2024-01-01T12:00:00Z"}
        ]
        
        result = await incident_service.update_status(1, "RESOLVED")
        
        assert result["status"] == "RESOLVED"
        assert "resolved_at" in result
    
    @pytest.mark.asyncio
    async def test_calculate_incident_priority(self, incident_service):
        """Test incident priority calculation"""
        # High severity fire should have high priority
        fire_incident = {
            "incident_type": "FIRE",
            "severity": "HIGH",
            "location_risk": "HIGH",
            "resource_availability": "LOW"
        }
        
        priority = incident_service.calculate_priority(fire_incident)
        assert priority >= 80  # Should be high priority
        
        # Low severity incident should have lower priority
        minor_incident = {
            "incident_type": "OTHER",
            "severity": "LOW",
            "location_risk": "LOW", 
            "resource_availability": "HIGH"
        }
        
        priority = incident_service.calculate_priority(minor_incident)
        assert priority <= 50  # Should be lower priority

class TestResourceService:
    """Test resource management service"""
    
    @pytest.fixture
    def resource_service(self, mock_supabase):
        """Create resource service instance"""
        from services.resource_service import ResourceService
        return ResourceService()
    
    @pytest.mark.asyncio
    async def test_find_available_resources(self, resource_service, mock_supabase):
        """Test finding available resources"""
        mock_resources = [
            {"id": 1, "type": "FIRE_TRUCK", "status": "AVAILABLE", "location": "Station A"},
            {"id": 2, "type": "AMBULANCE", "status": "AVAILABLE", "location": "Station B"},
            {"id": 3, "type": "FIRE_TRUCK", "status": "BUSY", "location": "Station C"}
        ]
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = mock_resources[:2]
        
        result = await resource_service.get_available_resources()
        
        assert len(result) == 2
        assert all(resource["status"] == "AVAILABLE" for resource in result)
    
    @pytest.mark.asyncio
    async def test_resource_assignment(self, resource_service, mock_supabase):
        """Test assigning resources to incidents"""
        assignment_data = {
            "resource_id": 1,
            "incident_id": 1,
            "assigned_by": "admin@example.com"
        }
        
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
            {**assignment_data, "id": 1, "assigned_at": "2024-01-01T00:00:00Z"}
        ]
        
        result = await resource_service.assign_resource(
            resource_id=1,
            incident_id=1,
            assigned_by="admin@example.com"
        )
        
        assert result["resource_id"] == 1
        assert result["incident_id"] == 1
    
    @pytest.mark.asyncio
    async def test_calculate_response_time(self, resource_service):
        """Test response time calculation"""
        resource_location = {"lat": 40.7128, "lng": -74.0060}  # NYC
        incident_location = {"lat": 40.7589, "lng": -73.9851}  # Times Square
        
        response_time = resource_service.calculate_response_time(
            resource_location, 
            incident_location
        )
        
        assert isinstance(response_time, (int, float))
        assert response_time > 0  # Should be positive
        assert response_time < 60  # Should be reasonable for NYC distances
