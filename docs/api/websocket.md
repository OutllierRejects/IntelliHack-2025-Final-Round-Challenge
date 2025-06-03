# WebSocket API

The WebSocket API provides real-time communication capabilities for live updates, notifications, and coordination between users and AI agents.

## Overview

WebSocket connections enable:

- **Real-time Notifications**: Instant updates on emergency requests, task assignments, and system alerts
- **Live Coordination**: Real-time communication between responders and affected individuals
- **Status Updates**: Live tracking of resource allocation and task progress
- **AI Agent Integration**: Direct communication with AI agents for automated responses

## Connection Management

### Establishing Connection

```javascript
// Connect to WebSocket with authentication
const token = localStorage.getItem('auth_token');
const socket = new WebSocket(`ws://localhost:8000/ws?token=${token}`);

socket.onopen = (event) => {
  console.log('WebSocket connected');
  // Send initial subscription preferences
  socket.send(JSON.stringify({
    type: 'subscribe',
    channels: ['emergency_alerts', 'task_updates', 'resource_changes']
  }));
};

socket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  handleWebSocketMessage(message);
};

socket.onclose = (event) => {
  console.log('WebSocket disconnected:', event.code, event.reason);
  // Implement reconnection logic
  setTimeout(reconnectWebSocket, 1000);
};

socket.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

### Authentication

WebSocket connections require authentication via JWT token:

```javascript
// Option 1: Query parameter
const socket = new WebSocket(`ws://localhost:8000/ws?token=${jwt_token}`);

// Option 2: Initial message after connection
socket.onopen = () => {
  socket.send(JSON.stringify({
    type: 'authenticate',
    token: jwt_token
  }));
};
```

## Message Types

### Subscription Management

```javascript
// Subscribe to specific channels
{
  "type": "subscribe",
  "channels": ["emergency_alerts", "task_updates", "resource_changes"],
  "filters": {
    "location": {
      "latitude": 6.9271,
      "longitude": 79.8612,
      "radius": 10000  // 10km radius
    },
    "priority": ["high", "critical"]
  }
}

// Unsubscribe from channels
{
  "type": "unsubscribe",
  "channels": ["resource_changes"]
}

// Get active subscriptions
{
  "type": "get_subscriptions"
}
```

### Emergency Alerts

Real-time emergency notifications:

```javascript
// Incoming emergency alert
{
  "type": "emergency_alert",
  "data": {
    "alert_id": "alert_001",
    "request_id": "req_789",
    "severity": "critical",
    "category": "medical_emergency",
    "location": {
      "latitude": 6.9271,
      "longitude": 79.8612,
      "address": "123 Main Street, Colombo"
    },
    "description": "Cardiac arrest - immediate medical assistance required",
    "required_skills": ["medical_assistance", "cpr"],
    "estimated_response_time": 300,  // seconds
    "contact": {
      "name": "Emergency Dispatcher",
      "phone": "+94112345678"
    },
    "timestamp": "2024-01-15T12:00:00Z"
  }
}

// Acknowledge emergency alert
{
  "type": "acknowledge_alert",
  "alert_id": "alert_001",
  "user_id": "user_001",
  "response": "accepting",  // accepting, declining, unavailable
  "estimated_arrival": "2024-01-15T12:15:00Z"
}
```

### Task Updates

Real-time task status changes:

```javascript
// Task assignment notification
{
  "type": "task_assigned",
  "data": {
    "task_id": "task_456",
    "assigned_to": "user_001",
    "title": "Medical Supply Distribution",
    "location": {
      "latitude": 6.9271,
      "longitude": 79.8612,
      "address": "Community Center, Kandy"
    },
    "priority": "high",
    "deadline": "2024-01-15T18:00:00Z",
    "contact": {
      "name": "Site Coordinator",
      "phone": "+94771234567"
    },
    "instructions": "Distribute medical supplies to affected families",
    "resources_allocated": ["supply_truck_001", "medical_kit_025"]
  }
}

// Task status update
{
  "type": "task_status_update",
  "data": {
    "task_id": "task_456",
    "old_status": "assigned",
    "new_status": "in_progress",
    "updated_by": "user_001",
    "location": {
      "latitude": 6.9271,
      "longitude": 79.8612
    },
    "progress_notes": "Arrived at location, beginning distribution",
    "timestamp": "2024-01-15T13:30:00Z"
  }
}

// Task completion notification
{
  "type": "task_completed",
  "data": {
    "task_id": "task_456",
    "completed_by": "user_001",
    "completion_time": "2024-01-15T16:45:00Z",
    "duration": "3.25 hours",
    "outcome": "successful",
    "families_assisted": 25,
    "supplies_distributed": {
      "medical_kits": 25,
      "water_bottles": 100,
      "emergency_food": 25
    },
    "feedback": "All families received necessary supplies. No additional medical needs identified.",
    "photos": ["task_456_completion_1.jpg", "task_456_completion_2.jpg"]
  }
}
```

### Resource Updates

Real-time resource status changes:

```javascript
// Resource availability change
{
  "type": "resource_status_change",
  "data": {
    "resource_id": "ambulance_007",
    "resource_type": "ambulance",
    "old_status": "available",
    "new_status": "allocated",
    "location": {
      "latitude": 6.9271,
      "longitude": 79.8612
    },
    "allocated_to": {
      "request_id": "req_789",
      "task_id": "task_123"
    },
    "estimated_duration": "2 hours",
    "contact": {
      "driver": "John Silva",
      "phone": "+94771234567"
    },
    "timestamp": "2024-01-15T14:00:00Z"
  }
}

// New resource available
{
  "type": "resource_available",
  "data": {
    "resource_id": "medical_team_alpha",
    "resource_type": "medical_team",
    "location": {
      "latitude": 6.9271,
      "longitude": 79.8612,
      "address": "Colombo General Hospital"
    },
    "capabilities": ["trauma", "pediatric", "cardiac"],
    "team_size": 4,
    "equipment": ["defibrillator", "trauma_kit", "medications"],
    "availability_window": {
      "start": "2024-01-15T14:00:00Z",
      "end": "2024-01-15T22:00:00Z"
    }
  }
}
```

### AI Agent Communication

Direct communication with AI agents:

```javascript
// Send message to AI agent
{
  "type": "ai_agent_request",
  "agent_type": "coordination_agent",
  "request": {
    "action": "optimize_resource_allocation",
    "parameters": {
      "region": "colombo_district",
      "emergency_type": "flood",
      "priority": "high"
    }
  }
}

// AI agent response
{
  "type": "ai_agent_response",
  "agent_type": "coordination_agent",
  "response": {
    "status": "completed",
    "recommendations": [
      {
        "action": "reallocate_ambulances",
        "from": "kandy_district",
        "to": "colombo_district",
        "quantity": 3,
        "reasoning": "Higher demand in Colombo due to flood impact"
      }
    ],
    "resource_optimization": {
      "efficiency_gain": "23%",
      "response_time_improvement": "12 minutes average"
    }
  }
}

// AI agent proactive notification
{
  "type": "ai_agent_alert",
  "agent_type": "prediction_agent",
  "alert": {
    "type": "resource_shortage_prediction",
    "severity": "medium",
    "location": "galle_district",
    "resource_type": "medical_supplies",
    "predicted_shortage_time": "2024-01-15T20:00:00Z",
    "confidence": 0.85,
    "recommended_actions": [
      "Dispatch additional medical supplies from Colombo",
      "Activate volunteer medical teams in the area"
    ]
  }
}
```

### Chat and Communication

Real-time messaging between users:

```javascript
// Send chat message
{
  "type": "chat_message",
  "to": "user_002",
  "message": "Arriving at location in 10 minutes. Do you need additional medical supplies?",
  "context": {
    "task_id": "task_456",
    "location": "kandy_site_alpha"
  }
}

// Receive chat message
{
  "type": "chat_message_received",
  "from": "user_001",
  "from_name": "John Silva",
  "message": "Arriving at location in 10 minutes. Do you need additional medical supplies?",
  "context": {
    "task_id": "task_456",
    "location": "kandy_site_alpha"
  },
  "timestamp": "2024-01-15T15:30:00Z"
}

// Broadcast message to group
{
  "type": "group_message",
  "group": "task_456_team",
  "message": "Weather update: Heavy rain expected in 2 hours. Prioritize indoor distributions.",
  "priority": "high",
  "sender": {
    "id": "user_admin",
    "name": "Command Center",
    "role": "coordinator"
  }
}
```

## Channel Types

### emergency_alerts
- Critical emergency notifications
- Immediate response required
- Location-based filtering available

### task_updates
- Task assignments and status changes
- Progress notifications
- Completion confirmations

### resource_changes
- Resource availability updates
- Allocation notifications
- Capacity changes

### ai_agent_updates
- AI agent recommendations
- Automated alerts and predictions
- System optimization notifications

### chat_messages
- Direct user communication
- Group messaging
- Coordination messages

### system_alerts
- System maintenance notifications
- Security alerts
- Performance warnings

## Connection States

### Connected
```javascript
{
  "type": "connection_established",
  "user_id": "user_001",
  "session_id": "session_abc123",
  "capabilities": ["chat", "notifications", "ai_agents"],
  "timestamp": "2024-01-15T12:00:00Z"
}
```

### Authenticated
```javascript
{
  "type": "authentication_success",
  "user_id": "user_001",
  "role": "volunteer",
  "permissions": ["task_updates", "emergency_alerts", "chat"],
  "session_expires": "2024-01-15T20:00:00Z"
}
```

## Error Handling

### Authentication Errors
```javascript
{
  "type": "error",
  "code": "AUTHENTICATION_FAILED",
  "message": "Invalid or expired token",
  "details": {
    "token_status": "expired",
    "expiry_time": "2024-01-15T10:00:00Z"
  }
}
```

### Subscription Errors
```javascript
{
  "type": "error",
  "code": "SUBSCRIPTION_FAILED",
  "message": "Invalid channel or insufficient permissions",
  "details": {
    "invalid_channels": ["admin_alerts"],
    "required_permission": "admin_access"
  }
}
```

### Rate Limiting
```javascript
{
  "type": "error",
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many messages sent",
  "details": {
    "limit": 100,
    "window": "1 minute",
    "retry_after": 30
  }
}
```

## Reconnection Strategy

```javascript
class WebSocketManager {
  constructor(url, token) {
    this.url = url;
    this.token = token;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.subscriptions = [];
  }
  
  connect() {
    this.socket = new WebSocket(`${this.url}?token=${this.token}`);
    
    this.socket.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      this.resubscribe();
    };
    
    this.socket.onclose = () => {
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        setTimeout(() => {
          this.reconnectAttempts++;
          this.connect();
        }, this.reconnectDelay * Math.pow(2, this.reconnectAttempts));
      }
    };
  }
  
  resubscribe() {
    if (this.subscriptions.length > 0) {
      this.socket.send(JSON.stringify({
        type: 'subscribe',
        channels: this.subscriptions
      }));
    }
  }
}
```

## Performance Optimization

### Message Batching
```javascript
// Batch multiple updates
{
  "type": "batch_update",
  "updates": [
    {
      "type": "task_status_update",
      "data": { /* task update */ }
    },
    {
      "type": "resource_status_change",
      "data": { /* resource update */ }
    }
  ]
}
```

### Heartbeat/Ping-Pong
```javascript
// Client ping
{
  "type": "ping",
  "timestamp": "2024-01-15T12:00:00Z"
}

// Server pong
{
  "type": "pong",
  "timestamp": "2024-01-15T12:00:00Z"
}
```

## Security Considerations

### Message Validation
- All incoming messages are validated against schemas
- User permissions checked for each channel subscription
- Rate limiting prevents abuse

### Data Encryption
- Sensitive data encrypted in transit
- User-specific channels for private communications
- Audit logging for security monitoring

### Access Control
- Role-based channel access
- Geographic filtering for location-sensitive data
- Time-based session management

## Best Practices

### Client Implementation
- Implement exponential backoff for reconnections
- Handle connection state changes gracefully
- Store critical messages locally during disconnections
- Use message acknowledgments for important updates

### Server Implementation
- Implement proper connection limits
- Use message queuing for reliability
- Monitor connection health
- Implement geographic message routing for scalability
