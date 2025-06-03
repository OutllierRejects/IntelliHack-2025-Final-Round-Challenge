# MCP Tools Reference

This document provides detailed information about the Model Context Protocol (MCP) tools available in the disaster response coordination system.

## Overview

The MCP server exposes 6 specialized tools for disaster response coordination. Each tool is designed to handle specific aspects of emergency management, from initial request processing to resource allocation.

## Available Tools

### 1. process_emergency_request

**Purpose**: Process and analyze incoming emergency requests using AI-powered triage and prioritization.

**Input Schema**:

```json
{
  "request_data": {
    "title": "string",
    "description": "string",
    "location": "string",
    "people_count": "number",
    "contact_phone": "string (optional)",
    "special_requirements": "string (optional)",
    "needs": ["array of strings"]
  }
}
```

**Output Schema**:

```json
{
  "request_id": "string",
  "priority": "critical|high|medium|low",
  "severity_score": "number (1-10)",
  "estimated_response_time": "string",
  "recommended_resources": ["array of resource types"],
  "assigned_responders": ["array of responder IDs"],
  "ai_analysis": {
    "risk_factors": ["array of identified risks"],
    "urgency_indicators": ["array of urgency markers"],
    "resource_requirements": "object"
  },
  "next_actions": ["array of recommended actions"]
}
```

**Usage Example**:

```python
result = await mcp_client.call_tool("process_emergency_request", {
  "request_data": {
    "title": "Building Fire on Main Street",
    "description": "Large fire at residential building, multiple people trapped",
    "location": "123 Main Street, Downtown",
    "people_count": 15,
    "contact_phone": "+1234567890",
    "needs": ["fire_suppression", "medical_assistance", "evacuation"]
  }
})
```

**AI Processing Logic**:

- Analyzes description for severity indicators
- Extracts location and resource requirements
- Calculates priority based on multiple factors
- Suggests optimal resource allocation
- Estimates response timeframes

---

### 2. get_agent_status

**Purpose**: Retrieve real-time status information for all AI agents in the system.

**Input Schema**:

```json
{
  "agent_names": ["array of agent names (optional)"],
  "include_metrics": "boolean (default: true)"
}
```

**Output Schema**:

```json
{
  "agents": {
    "agent_name": {
      "status": "active|idle|busy|error",
      "current_task": "string",
      "last_activity": "ISO datetime",
      "processed_requests": "number",
      "success_rate": "number (0-1)",
      "average_processing_time": "number (seconds)",
      "active_assignments": "number",
      "capabilities": ["array of capabilities"],
      "performance_metrics": {
        "requests_per_hour": "number",
        "error_rate": "number",
        "response_time_p95": "number"
      }
    }
  },
  "system_health": {
    "total_active_agents": "number",
    "system_load": "number",
    "queue_length": "number"
  }
}
```

**Usage Example**:

```python
status = await mcp_client.call_tool("get_agent_status", {
  "agent_names": ["emergency_agent", "resource_agent"],
  "include_metrics": True
})
```

---

### 3. get_active_requests

**Purpose**: Retrieve and filter active emergency requests based on various criteria.

**Input Schema**:

```json
{
  "filters": {
    "status": ["pending", "in_progress", "assigned"],
    "priority": ["critical", "high", "medium", "low"],
    "location": "string (optional)",
    "request_type": ["medical", "fire", "natural_disaster", "security"],
    "assigned_to": "string (user_id, optional)",
    "created_after": "ISO datetime (optional)",
    "created_before": "ISO datetime (optional)"
  },
  "sort_by": "priority|created_at|location",
  "sort_order": "asc|desc",
  "limit": "number (default: 50)",
  "include_analytics": "boolean (default: false)"
}
```

**Output Schema**:

```json
{
  "requests": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "status": "string",
      "priority": "string",
      "location": "string",
      "people_count": "number",
      "created_at": "ISO datetime",
      "updated_at": "ISO datetime",
      "assigned_responders": ["array of user objects"],
      "required_resources": ["array of resource types"],
      "estimated_completion": "ISO datetime",
      "progress_percentage": "number"
    }
  ],
  "total_count": "number",
  "analytics": {
    "priority_distribution": "object",
    "status_distribution": "object",
    "average_response_time": "number",
    "critical_requests_count": "number"
  }
}
```

**Usage Example**:

```python
active_requests = await mcp_client.call_tool("get_active_requests", {
  "filters": {
    "status": ["pending", "in_progress"],
    "priority": ["critical", "high"]
  },
  "sort_by": "priority",
  "sort_order": "desc",
  "limit": 20,
  "include_analytics": True
})
```

---

### 4. assign_volunteer_to_task

**Purpose**: Intelligently assign volunteers to tasks based on skills, availability, location, and workload.

**Input Schema**:

```json
{
  "task_id": "string",
  "volunteer_criteria": {
    "required_skills": ["array of skill names"],
    "location_radius": "number (km, optional)",
    "availability_required": "boolean (default: true)",
    "experience_level": "beginner|intermediate|advanced|expert",
    "max_current_tasks": "number (default: 3)"
  },
  "assignment_preferences": {
    "prefer_nearby": "boolean (default: true)",
    "prefer_experienced": "boolean (default: true)",
    "load_balance": "boolean (default: true)"
  },
  "auto_assign": "boolean (default: false)"
}
```

**Output Schema**:

```json
{
  "recommended_volunteers": [
    {
      "volunteer_id": "string",
      "user": {
        "id": "string",
        "full_name": "string",
        "email": "string",
        "skills": ["array of skills"],
        "experience_level": "string",
        "location": "string"
      },
      "match_score": "number (0-100)",
      "distance_km": "number",
      "current_task_count": "number",
      "availability_status": "boolean",
      "match_reasons": ["array of matching criteria"],
      "estimated_travel_time": "number (minutes)"
    }
  ],
  "assignment_result": {
    "assigned": "boolean",
    "assigned_to": "string (volunteer_id if assigned)",
    "assignment_reason": "string",
    "estimated_start_time": "ISO datetime"
  },
  "assignment_analytics": {
    "total_candidates": "number",
    "top_match_score": "number",
    "average_distance": "number"
  }
}
```

**Usage Example**:

```python
assignment = await mcp_client.call_tool("assign_volunteer_to_task", {
  "task_id": "task_123",
  "volunteer_criteria": {
    "required_skills": ["first_aid", "search_rescue"],
    "location_radius": 10,
    "experience_level": "intermediate"
  },
  "assignment_preferences": {
    "prefer_nearby": True,
    "load_balance": True
  },
  "auto_assign": True
})
```

---

### 5. get_available_resources

**Purpose**: Query and analyze available resources for emergency response with real-time inventory tracking.

**Input Schema**:

```json
{
  "resource_filters": {
    "types": ["medical", "food", "shelter", "transportation", "equipment"],
    "location": "string (optional)",
    "location_radius": "number (km, optional)",
    "minimum_quantity": "number (optional)",
    "available_only": "boolean (default: true)"
  },
  "include_details": {
    "consumption_history": "boolean (default: false)",
    "supplier_info": "boolean (default: false)",
    "expiry_tracking": "boolean (default: true)"
  },
  "sort_by": "quantity|distance|expiry_date|last_updated",
  "group_by": "type|location|supplier"
}
```

**Output Schema**:

```json
{
  "resources": [
    {
      "id": "string",
      "name": "string",
      "type": "string",
      "description": "string",
      "quantity": "number",
      "unit": "string",
      "location": "string",
      "status": "available|low_stock|out_of_stock|reserved",
      "last_updated": "ISO datetime",
      "expiry_date": "ISO datetime (optional)",
      "cost_per_unit": "number",
      "supplier": "string",
      "distance_km": "number (if location filter provided)"
    }
  ],
  "resource_summary": {
    "total_resources": "number",
    "by_type": "object",
    "by_status": "object",
    "low_stock_alerts": ["array of resource IDs"],
    "expiring_soon": ["array of resource IDs"]
  },
  "allocation_suggestions": [
    {
      "resource_id": "string",
      "suggested_allocation": "number",
      "reason": "string",
      "urgency": "high|medium|low"
    }
  ]
}
```

**Usage Example**:

```python
resources = await mcp_client.call_tool("get_available_resources", {
  "resource_filters": {
    "types": ["medical", "food"],
    "location": "downtown",
    "location_radius": 15,
    "available_only": True
  },
  "include_details": {
    "expiry_tracking": True,
    "supplier_info": True
  },
  "sort_by": "quantity",
  "group_by": "type"
})
```

---

### 6. prioritize_requests

**Purpose**: Re-evaluate and prioritize emergency requests using advanced AI algorithms and current system state.

**Input Schema**:

```json
{
  "request_ids": [
    "array of request IDs (optional - if empty, processes all active)"
  ],
  "prioritization_criteria": {
    "urgency_weight": "number (0-1, default: 0.4)",
    "severity_weight": "number (0-1, default: 0.3)",
    "resource_availability_weight": "number (0-1, default: 0.2)",
    "response_capacity_weight": "number (0-1, default: 0.1)"
  },
  "context_factors": {
    "current_time": "ISO datetime",
    "weather_conditions": "string (optional)",
    "available_responders": "number",
    "system_load": "number (0-1)"
  },
  "update_priorities": "boolean (default: true)"
}
```

**Output Schema**:

```json
{
  "prioritized_requests": [
    {
      "request_id": "string",
      "original_priority": "string",
      "new_priority": "string",
      "priority_score": "number (0-100)",
      "urgency_score": "number",
      "severity_score": "number",
      "resource_availability_score": "number",
      "response_capacity_score": "number",
      "priority_change_reason": "string",
      "estimated_wait_time": "number (minutes)",
      "recommended_actions": ["array of actions"]
    }
  ],
  "prioritization_summary": {
    "total_requests_processed": "number",
    "priority_changes": "number",
    "critical_requests": "number",
    "average_priority_score": "number",
    "system_recommendations": ["array of system-level recommendations"]
  },
  "resource_allocation_impact": {
    "over_allocated_resources": ["array of resource types"],
    "under_allocated_resources": ["array of resource types"],
    "optimization_suggestions": ["array of suggestions"]
  }
}
```

**Usage Example**:

```python
prioritization = await mcp_client.call_tool("prioritize_requests", {
  "prioritization_criteria": {
    "urgency_weight": 0.5,
    "severity_weight": 0.3,
    "resource_availability_weight": 0.2
  },
  "context_factors": {
    "current_time": "2024-01-15T14:30:00Z",
    "available_responders": 25,
    "system_load": 0.7
  },
  "update_priorities": True
})
```

## Tool Integration Examples

### Complete Emergency Response Workflow

```python
async def handle_emergency_workflow(request_data):
    # 1. Process initial request
    processed_request = await mcp_client.call_tool("process_emergency_request", {
        "request_data": request_data
    })

    # 2. Get current system status
    agent_status = await mcp_client.call_tool("get_agent_status", {
        "include_metrics": True
    })

    # 3. Check available resources
    resources = await mcp_client.call_tool("get_available_resources", {
        "resource_filters": {
            "types": processed_request["recommended_resources"],
            "available_only": True
        }
    })

    # 4. Assign volunteers if tasks are created
    if processed_request.get("tasks_created"):
        for task_id in processed_request["tasks_created"]:
            assignment = await mcp_client.call_tool("assign_volunteer_to_task", {
                "task_id": task_id,
                "auto_assign": True
            })

    # 5. Re-prioritize all requests
    prioritization = await mcp_client.call_tool("prioritize_requests", {
        "update_priorities": True
    })

    return {
        "request": processed_request,
        "resources": resources,
        "prioritization": prioritization
    }
```

### Real-time Monitoring Dashboard

```python
async def get_dashboard_data():
    # Get all active requests
    active_requests = await mcp_client.call_tool("get_active_requests", {
        "include_analytics": True,
        "limit": 100
    })

    # Get agent status
    agents = await mcp_client.call_tool("get_agent_status", {
        "include_metrics": True
    })

    # Get resource status
    resources = await mcp_client.call_tool("get_available_resources", {
        "include_details": {
            "expiry_tracking": True
        },
        "group_by": "type"
    })

    return {
        "requests": active_requests,
        "agents": agents,
        "resources": resources,
        "timestamp": datetime.utcnow().isoformat()
    }
```

## Error Handling

### Common Error Responses

```json
{
  "error": true,
  "error_code": "INVALID_INPUT",
  "message": "Invalid request data provided",
  "details": {
    "field": "request_data.people_count",
    "issue": "Must be a positive integer"
  }
}
```

### Error Codes

- `INVALID_INPUT`: Input validation failed
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `AGENT_UNAVAILABLE`: Required AI agent is not responding
- `DATABASE_ERROR`: Database operation failed
- `RATE_LIMIT_EXCEEDED`: Too many requests in time window
- `PERMISSION_DENIED`: Insufficient permissions for operation

## Performance Considerations

### Caching Strategy

- Agent status cached for 30 seconds
- Resource data cached for 5 minutes
- Request prioritization cached for 2 minutes
- Tool responses include cache timestamps

### Rate Limiting

- Maximum 100 requests per minute per client
- Burst limit of 20 requests per 10 seconds
- Priority tools have higher rate limits

### Optimization Tips

- Use filters to limit data returned
- Enable caching for frequently accessed data
- Batch operations when possible
- Monitor tool performance metrics

This comprehensive tool reference enables effective integration and usage of the MCP server in disaster response scenarios.
