"""
Test suite for AGNO agents - Intake, Prioritization, Assignment, and Communication agents
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
import json
from datetime import datetime, timezone

from agno_agents.intake_agent import IntakeAgent
from agno_agents.prioritization_agent import PrioritizationAgent
from agno_agents.assignment_agent import AssignmentAgent
from agno_agents.communication_agent import CommunicationAgent

class TestIntakeAgent:
    """Test the Intake Agent functionality"""
    
    @pytest.fixture
    def intake_agent(self, mock_openai, mock_supabase):
        """Create an intake agent instance for testing"""
        return IntakeAgent()
    
    @pytest.mark.asyncio
    async def test_process_disaster_request(self, intake_agent, mock_openai):
        """Test processing a disaster request"""
        # Mock request data
        request_data = {
            "description": "Fire emergency in downtown area",
            "location": "Main Street, Downtown",
            "contact_info": "john@example.com",
            "urgency_level": "high"
        }
        
        # Mock OpenAI response
        mock_openai.chat.completions.create.return_value.choices = [
            Mock(message=Mock(content=json.dumps({
                "priority": "HIGH",
                "category": "FIRE",
                "estimated_resources": ["fire_truck", "ambulance"],
                "immediate_actions": ["evacuate_area", "contact_fire_dept"]
            })))
        ]
        
        result = await intake_agent.process_request(request_data)
        
        assert result is not None
        assert result["status"] == "processed"
        assert "priority" in result
    
    @pytest.mark.asyncio
    async def test_validate_request_data(self, intake_agent):
        """Test request data validation"""
        valid_request = {
            "description": "Emergency situation",
            "location": "Test Location",
            "contact_info": "test@example.com"
        }
        
        invalid_request = {
            "description": "",  # Empty description
            "location": "Test Location"
            # Missing contact_info
        }
        
        assert intake_agent.validate_request(valid_request) == True
        assert intake_agent.validate_request(invalid_request) == False

class TestPrioritizationAgent:
    """Test the Prioritization Agent functionality"""
    
    @pytest.fixture
    def prioritization_agent(self, mock_openai, mock_supabase):
        """Create a prioritization agent instance"""
        return PrioritizationAgent()
    
    @pytest.mark.asyncio
    async def test_prioritize_requests(self, prioritization_agent, mock_openai):
        """Test request prioritization"""
        requests = [
            {"id": 1, "type": "FIRE", "severity": "HIGH", "location": "Downtown"},
            {"id": 2, "type": "FLOOD", "severity": "MEDIUM", "location": "Suburb"},
            {"id": 3, "type": "MEDICAL", "severity": "CRITICAL", "location": "Hospital"}
        ]
        
        # Mock OpenAI response for prioritization
        mock_openai.chat.completions.create.return_value.choices = [
            Mock(message=Mock(content=json.dumps([
                {"id": 3, "priority_score": 95, "reasoning": "Critical medical emergency"},
                {"id": 1, "priority_score": 80, "reasoning": "High severity fire"},
                {"id": 2, "priority_score": 60, "reasoning": "Medium severity flood"}
            ])))
        ]
        
        result = await prioritization_agent.prioritize(requests)
        
        assert len(result) == 3
        assert result[0]["id"] == 3  # Medical should be highest priority
        assert result[0]["priority_score"] == 95

class TestAssignmentAgent:
    """Test the Assignment Agent functionality"""
    
    @pytest.fixture
    def assignment_agent(self, mock_openai, mock_supabase):
        """Create an assignment agent instance"""
        return AssignmentAgent()
    
    @pytest.mark.asyncio
    async def test_assign_resources(self, assignment_agent, mock_openai):
        """Test resource assignment to requests"""
        request = {
            "id": 1,
            "type": "FIRE",
            "location": "Downtown",
            "priority": "HIGH"
        }
        
        available_resources = [
            {"id": 1, "type": "FIRE_TRUCK", "location": "Station A", "status": "available"},
            {"id": 2, "type": "AMBULANCE", "location": "Station B", "status": "available"},
            {"id": 3, "type": "POLICE_CAR", "location": "Station C", "status": "busy"}
        ]
        
        # Mock OpenAI response for assignment
        mock_openai.chat.completions.create.return_value.choices = [
            Mock(message=Mock(content=json.dumps({
                "assignments": [
                    {"resource_id": 1, "reasoning": "Fire truck needed for fire emergency"},
                    {"resource_id": 2, "reasoning": "Ambulance for potential injuries"}
                ],
                "estimated_response_time": "8 minutes"
            })))
        ]
        
        result = await assignment_agent.assign(request, available_resources)
        
        assert "assignments" in result
        assert len(result["assignments"]) == 2
        assert result["assignments"][0]["resource_id"] == 1

class TestCommunicationAgent:
    """Test the Communication Agent functionality"""
    
    @pytest.fixture
    def communication_agent(self, mock_openai, mock_supabase):
        """Create a communication agent instance"""
        return CommunicationAgent()
    
    @pytest.mark.asyncio
    async def test_generate_notifications(self, communication_agent, mock_openai):
        """Test notification generation"""
        incident = {
            "id": 1,
            "type": "FIRE",
            "location": "Downtown",
            "status": "ASSIGNED",
            "assigned_resources": ["Fire Truck #1", "Ambulance #2"]
        }
        
        stakeholders = [
            {"type": "REQUESTER", "contact": "john@example.com"},
            {"type": "RESPONDER", "contact": "fire@dept.gov"},
            {"type": "VOLUNTEER", "contact": "volunteer@org.com"}
        ]
        
        # Mock OpenAI response for communication
        mock_openai.chat.completions.create.return_value.choices = [
            Mock(message=Mock(content=json.dumps({
                "notifications": [
                    {
                        "recipient": "john@example.com",
                        "message": "Your fire emergency report has been received and resources are en route.",
                        "channel": "email"
                    },
                    {
                        "recipient": "fire@dept.gov",
                        "message": "Fire emergency at Downtown - Fire Truck #1 and Ambulance #2 assigned.",
                        "channel": "sms"
                    }
                ]
            })))
        ]
        
        result = await communication_agent.generate_notifications(incident, stakeholders)
        
        assert "notifications" in result
        assert len(result["notifications"]) >= 1
        assert result["notifications"][0]["recipient"] == "john@example.com"
    
    @pytest.mark.asyncio
    async def test_send_notification(self, communication_agent):
        """Test sending individual notifications"""
        notification = {
            "recipient": "test@example.com",
            "message": "Test emergency notification",
            "channel": "email"
        }
        
        with patch('services.notification_service.send_email') as mock_send:
            mock_send.return_value = True
            result = await communication_agent.send_notification(notification)
            assert result["status"] == "sent"
            mock_send.assert_called_once()

class TestAgentCoordination:
    """Test the coordination between different agents"""
    
    @pytest.mark.asyncio
    async def test_full_agent_workflow(self, mock_openai, mock_supabase):
        """Test the complete agent workflow from intake to communication"""
        # This would test the full pipeline
        initial_request = {
            "description": "Building fire with people trapped",
            "location": "123 Main St",
            "contact_info": "emergency@caller.com",
            "urgency_level": "critical"
        }
        
        # Step 1: Intake
        intake_agent = IntakeAgent()
        processed_request = await intake_agent.process_request(initial_request)
        assert processed_request["status"] == "processed"
        
        # Step 2: Prioritization  
        prioritization_agent = PrioritizationAgent()
        prioritized = await prioritization_agent.prioritize([processed_request])
        assert len(prioritized) == 1
        
        # Step 3: Assignment
        assignment_agent = AssignmentAgent()
        mock_resources = [
            {"id": 1, "type": "FIRE_TRUCK", "status": "available"},
            {"id": 2, "type": "AMBULANCE", "status": "available"}
        ]
        assigned = await assignment_agent.assign(prioritized[0], mock_resources)
        assert "assignments" in assigned
        
        # Step 4: Communication
        communication_agent = CommunicationAgent()
        mock_stakeholders = [{"type": "REQUESTER", "contact": "emergency@caller.com"}]
        communications = await communication_agent.generate_notifications(assigned, mock_stakeholders)
        assert "notifications" in communications
