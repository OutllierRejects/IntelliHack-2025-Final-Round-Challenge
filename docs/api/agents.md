# AI Agents API

The AI Agents API provides access to intelligent automation capabilities for disaster response coordination, including emergency processing, resource optimization, and predictive analytics.

## Overview

The system includes multiple specialized AI agents:

- **Emergency Processing Agent**: Analyzes and categorizes emergency requests
- **Resource Optimization Agent**: Optimizes resource allocation and distribution
- **Coordination Agent**: Manages task assignments and workflow optimization
- **Prediction Agent**: Provides predictive analytics and early warnings
- **Communication Agent**: Handles automated notifications and messaging

## Agent Types

### Emergency Processing Agent

Analyzes incoming emergency requests and provides intelligent categorization and prioritization.

```http
POST /api/ai-agents/emergency-processor/analyze
```

**Request Body:**
```json
{
  "request_id": "req_789",
  "description": "House fire on Galle Road, family trapped on second floor",
  "location": {
    "latitude": 6.9271,
    "longitude": 79.8612,
    "address": "45 Galle Road, Colombo 03"
  },
  "reporter": {
    "name": "Maria Silva",
    "phone": "+94771234567",
    "relationship": "neighbor"
  },
  "media": [
    {
      "type": "image",
      "url": "/uploads/emergency_photo_001.jpg"
    },
    {
      "type": "audio",
      "url": "/uploads/emergency_audio_001.wav",
      "transcription": "Help, there's a fire and people are trapped upstairs!"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis_id": "analysis_001",
    "emergency_category": "structural_fire",
    "severity": "critical",
    "confidence": 0.95,
    "priority_score": 95,
    "risk_assessment": {
      "life_threat": "high",
      "property_damage": "severe",
      "spread_risk": "high",
      "weather_impact": "low"
    },
    "required_resources": [
      {
        "type": "fire_truck",
        "quantity": 2,
        "urgency": "immediate"
      },
      {
        "type": "ambulance",
        "quantity": 1,
        "urgency": "immediate"
      },
      {
        "type": "rescue_team",
        "quantity": 1,
        "urgency": "immediate"
      }
    ],
    "response_timeline": {
      "initial_response": "5 minutes",
      "resource_deployment": "8 minutes",
      "estimated_resolution": "45 minutes"
    },
    "safety_protocols": [
      "Evacuate surrounding buildings",
      "Establish safety perimeter",
      "Monitor for structural collapse"
    ],
    "ai_recommendations": [
      "Deploy ladder truck for second-floor rescue",
      "Coordinate with power company for electrical shutdown",
      "Alert nearby hospitals for potential casualties"
    ]
  }
}
```

### Resource Optimization Agent

Optimizes resource allocation based on current demand and availability.

```http
POST /api/ai-agents/resource-optimizer/optimize
```

**Request Body:**
```json
{
  "optimization_type": "emergency_response",
  "region": "western_province",
  "parameters": {
    "active_emergencies": [
      {
        "request_id": "req_789",
        "category": "fire",
        "priority": "critical",
        "location": {"latitude": 6.9271, "longitude": 79.8612}
      },
      {
        "request_id": "req_790",
        "category": "medical",
        "priority": "high",
        "location": {"latitude": 6.9319, "longitude": 79.8478}
      }
    ],
    "available_resources": [
      {
        "resource_id": "fire_truck_001",
        "type": "fire_truck",
        "location": {"latitude": 6.9200, "longitude": 79.8500},
        "status": "available"
      }
    ],
    "constraints": {
      "max_response_time": 600,
      "minimum_coverage": 0.8
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "optimization_id": "opt_001",
    "allocation_plan": [
      {
        "resource_id": "fire_truck_001",
        "assigned_to": "req_789",
        "deployment_time": "2024-01-15T12:05:00Z",
        "estimated_arrival": "2024-01-15T12:13:00Z",
        "route": {
          "distance": "3.2 km",
          "duration": "8 minutes",
          "traffic_conditions": "moderate"
        }
      }
    ],
    "performance_metrics": {
      "average_response_time": "7.5 minutes",
      "resource_utilization": 0.85,
      "coverage_achieved": 0.92
    },
    "alternative_scenarios": [
      {
        "scenario": "if_additional_fire_truck_available",
        "improvement": "3 minutes faster response"
      }
    ],
    "recommendations": [
      "Consider repositioning ambulance_003 to central location",
      "Request additional fire truck from neighboring district"
    ]
  }
}
```

### Coordination Agent

Manages task assignments and workflow optimization.

```http
POST /api/ai-agents/coordinator/assign-tasks
```

**Request Body:**
```json
{
  "emergency_request": "req_789",
  "available_volunteers": [
    {
      "user_id": "user_001",
      "skills": ["first_aid", "search_rescue"],
      "location": {"latitude": 6.9271, "longitude": 79.8612},
      "availability": "immediate"
    },
    {
      "user_id": "user_002",
      "skills": ["medical_assistance", "translation"],
      "location": {"latitude": 6.9300, "longitude": 79.8500},
      "availability": "30_minutes"
    }
  ],
  "task_requirements": {
    "skills_needed": ["first_aid", "crowd_control"],
    "personnel_count": 3,
    "duration_estimate": "2 hours"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "assignment_id": "assign_001",
    "task_assignments": [
      {
        "task_id": "task_456",
        "assigned_to": "user_001",
        "role": "team_leader",
        "skills_utilized": ["first_aid", "search_rescue"],
        "estimated_arrival": "2024-01-15T12:08:00Z",
        "instructions": "Lead rescue operations on second floor"
      },
      {
        "task_id": "task_457",
        "assigned_to": "user_002",
        "role": "medical_support",
        "skills_utilized": ["medical_assistance"],
        "estimated_arrival": "2024-01-15T12:15:00Z",
        "instructions": "Provide medical triage for evacuees"
      }
    ],
    "coordination_plan": {
      "meeting_point": {
        "latitude": 6.9271,
        "longitude": 79.8612,
        "description": "Corner of Galle Road and Marine Drive"
      },
      "communication_channel": "emergency_channel_001",
      "backup_assignments": [
        {
          "if": "user_001_unavailable",
          "then": "assign_user_003"
        }
      ]
    },
    "success_probability": 0.91
  }
}
```

### Prediction Agent

Provides predictive analytics and early warnings.

```http
POST /api/ai-agents/predictor/forecast
```

**Request Body:**
```json
{
  "prediction_type": "demand_forecast",
  "timeframe": "24_hours",
  "region": "colombo_district",
  "parameters": {
    "weather_data": {
      "current_conditions": "heavy_rain",
      "forecast": "continued_rain_12h"
    },
    "historical_data": true,
    "current_capacity": {
      "ambulances": 15,
      "fire_trucks": 8,
      "volunteers": 120
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "prediction_id": "pred_001",
    "forecast": {
      "timeframe": "next_24_hours",
      "predicted_incidents": [
        {
          "type": "flooding",
          "probability": 0.78,
          "expected_count": "12-18 incidents",
          "peak_time": "18:00-22:00",
          "affected_areas": ["low_lying_areas", "drainage_prone_zones"]
        },
        {
          "type": "traffic_accidents",
          "probability": 0.65,
          "expected_count": "8-12 incidents",
          "contributing_factors": ["reduced_visibility", "slippery_roads"]
        }
      ],
      "resource_demand": {
        "ambulances": {
          "current": 15,
          "predicted_needed": 22,
          "shortage": 7
        },
        "rescue_boats": {
          "current": 4,
          "predicted_needed": 8,
          "shortage": 4
        }
      },
      "hotspots": [
        {
          "location": "Wellawatte area",
          "risk_level": "high",
          "predicted_incidents": 5,
          "recommended_staging": {
            "ambulances": 2,
            "rescue_team": 1
          }
        }
      ]
    },
    "recommendations": [
      "Pre-position additional ambulances in high-risk areas",
      "Activate volunteer flood response teams",
      "Coordinate with meteorology department for updates",
      "Alert hospitals to prepare for increased casualties"
    ],
    "confidence_level": 0.82,
    "last_updated": "2024-01-15T12:00:00Z"
  }
}
```

### Communication Agent

Handles automated notifications and messaging.

```http
POST /api/ai-agents/communicator/send-notifications
```

**Request Body:**
```json
{
  "notification_type": "emergency_alert",
  "target_audience": {
    "roles": ["volunteers", "first_responders"],
    "location": {
      "latitude": 6.9271,
      "longitude": 79.8612,
      "radius": 5000
    },
    "skills": ["first_aid", "search_rescue"]
  },
  "message_template": "emergency_response",
  "variables": {
    "incident_type": "house_fire",
    "location": "45 Galle Road, Colombo 03",
    "urgency": "critical",
    "skills_needed": ["first_aid", "search_rescue"]
  },
  "channels": ["sms", "push_notification", "websocket"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "notification_id": "notif_001",
    "recipients": [
      {
        "user_id": "user_001",
        "channels_sent": ["sms", "push_notification"],
        "delivery_status": "sent",
        "estimated_delivery": "2024-01-15T12:01:00Z"
      },
      {
        "user_id": "user_002",
        "channels_sent": ["push_notification", "websocket"],
        "delivery_status": "sent",
        "estimated_delivery": "2024-01-15T12:01:00Z"
      }
    ],
    "message_content": {
      "sms": "🚨 EMERGENCY: House fire at 45 Galle Road, Colombo 03. First aid & search rescue skills needed. Respond if available.",
      "push": {
        "title": "Emergency Response Needed",
        "body": "House fire - First aid & search rescue required",
        "data": {
          "request_id": "req_789",
          "location": "45 Galle Road, Colombo 03"
        }
      }
    },
    "delivery_metrics": {
      "total_sent": 25,
      "delivery_rate": 0.96,
      "response_rate": 0.68,
      "average_response_time": "3.2 minutes"
    }
  }
}
```

## Agent Status and Monitoring

### Get Agent Status

```http
GET /api/ai-agents/status
```

**Response:**
```json
{
  "success": true,
  "data": {
    "agents": [
      {
        "name": "emergency_processor",
        "status": "active",
        "current_load": 0.75,
        "processed_today": 145,
        "average_processing_time": "2.3 seconds",
        "success_rate": 0.97,
        "last_health_check": "2024-01-15T12:00:00Z"
      },
      {
        "name": "resource_optimizer",
        "status": "active",
        "current_optimizations": 3,
        "optimization_success_rate": 0.91,
        "average_improvement": "15% efficiency gain",
        "last_optimization": "2024-01-15T11:45:00Z"
      }
    ],
    "system_health": {
      "overall_status": "healthy",
      "response_time": "1.8 seconds average",
      "error_rate": 0.03,
      "uptime": "99.7%"
    }
  }
}
```

### Agent Performance Metrics

```http
GET /api/ai-agents/{agent_name}/metrics
```

**Response:**
```json
{
  "success": true,
  "data": {
    "agent_name": "emergency_processor",
    "time_period": "last_24_hours",
    "metrics": {
      "total_requests": 145,
      "successful_analyses": 140,
      "failed_analyses": 5,
      "average_processing_time": "2.3 seconds",
      "accuracy_score": 0.94,
      "categories_identified": {
        "medical": 45,
        "fire": 28,
        "natural_disaster": 35,
        "accident": 32
      },
      "confidence_distribution": {
        "high_confidence": 0.78,
        "medium_confidence": 0.18,
        "low_confidence": 0.04
      }
    },
    "performance_trends": {
      "processing_time": "improving",
      "accuracy": "stable",
      "throughput": "increasing"
    }
  }
}
```

## Agent Training and Learning

### Feedback Submission

```http
POST /api/ai-agents/feedback
```

**Request Body:**
```json
{
  "agent_name": "emergency_processor",
  "analysis_id": "analysis_001",
  "feedback": {
    "accuracy_rating": 4,
    "category_correct": true,
    "severity_correct": true,
    "resource_recommendations": "partially_correct",
    "notes": "Category and severity were accurate, but recommended 1 extra ambulance than needed",
    "actual_outcome": {
      "resources_used": [
        {"type": "fire_truck", "quantity": 2},
        {"type": "ambulance", "quantity": 1}
      ],
      "resolution_time": "35 minutes",
      "casualties": 0
    }
  },
  "feedback_source": {
    "user_id": "user_admin",
    "role": "incident_commander",
    "experience_level": "expert"
  }
}
```

### Model Updates

```http
POST /api/ai-agents/{agent_name}/retrain
```

Trigger retraining of AI models with new data (admin only).

## Integration Examples

### Emergency Request Processing Workflow

```javascript
// Process emergency request through AI agent
const processEmergency = async (emergencyData) => {
  try {
    // Step 1: Analyze with AI agent
    const analysis = await fetch('/api/ai-agents/emergency-processor/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(emergencyData)
    });
    
    const analysisResult = await analysis.json();
    
    // Step 2: Get resource optimization
    const optimization = await fetch('/api/ai-agents/resource-optimizer/optimize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        optimization_type: 'emergency_response',
        analysis: analysisResult.data
      })
    });
    
    const optimizationResult = await optimization.json();
    
    // Step 3: Coordinate task assignments
    const coordination = await fetch('/api/ai-agents/coordinator/assign-tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        emergency_request: emergencyData.request_id,
        resource_plan: optimizationResult.data
      })
    });
    
    return await coordination.json();
    
  } catch (error) {
    console.error('AI processing failed:', error);
    throw error;
  }
};
```

### Real-time Agent Communication

```javascript
// WebSocket integration with AI agents
const socket = new WebSocket('ws://localhost:8000/ws');

// Listen for AI agent updates
socket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  if (message.type === 'ai_agent_response') {
    handleAgentResponse(message.data);
  } else if (message.type === 'ai_agent_alert') {
    handleAgentAlert(message.data);
  }
};

// Request AI agent analysis
const requestAgentAnalysis = (data) => {
  socket.send(JSON.stringify({
    type: 'ai_agent_request',
    agent_type: 'emergency_processor',
    request: data
  }));
};
```

## Error Handling

### Agent Unavailable
```json
{
  "success": false,
  "error": {
    "code": "AGENT_UNAVAILABLE",
    "message": "Emergency processing agent is currently unavailable",
    "details": {
      "agent_status": "maintenance",
      "estimated_availability": "2024-01-15T13:00:00Z"
    }
  }
}
```

### Processing Failed
```json
{
  "success": false,
  "error": {
    "code": "PROCESSING_FAILED",
    "message": "Unable to analyze emergency request",
    "details": {
      "reason": "insufficient_data",
      "missing_fields": ["location", "description"],
      "retry_possible": true
    }
  }
}
```

### Rate Limit Exceeded
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests to AI agent",
    "details": {
      "limit": 100,
      "window": "1 minute",
      "retry_after": 30
    }
  }
}
```

## Best Practices

### Agent Utilization
- **Load Balancing**: Distribute requests across multiple agent instances
- **Caching**: Cache frequently accessed predictions and analyses
- **Fallback Strategies**: Implement manual processing when agents are unavailable
- **Performance Monitoring**: Track agent response times and accuracy

### Data Quality
- **Input Validation**: Ensure high-quality input data for better results
- **Feedback Loops**: Continuously improve agents with outcome feedback
- **Data Enrichment**: Provide context and historical data when available
- **Error Handling**: Gracefully handle agent failures and partial results

### Integration Patterns
- **Asynchronous Processing**: Use async patterns for long-running analyses
- **Event-Driven Architecture**: Trigger agent actions based on system events
- **Human-in-the-Loop**: Combine AI recommendations with human oversight
- **Continuous Learning**: Update models based on real-world outcomes
