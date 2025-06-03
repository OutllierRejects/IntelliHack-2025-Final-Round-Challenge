# Resources API

The Resources API manages emergency response resources including medical supplies, vehicles, equipment, and personnel allocation.

## Overview

Resources are critical components of disaster response operations. The API provides functionality for:

- Resource inventory management
- Real-time availability tracking
- Allocation and assignment
- Capacity planning
- Location-based resource discovery

## Endpoints

### List Resources

```http
GET /api/resources
```

Retrieve all available resources with filtering options.

**Query Parameters:**
- `type` (string, optional): Filter by resource type (medical_supplies, vehicles, equipment, personnel)
- `location` (string, optional): Filter by location coordinates or area
- `status` (string, optional): Filter by availability status (available, allocated, maintenance)
- `capacity` (number, optional): Minimum capacity requirement

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "resource_001",
      "type": "ambulance",
      "category": "vehicles",
      "name": "Ambulance Unit 7",
      "location": {
        "latitude": 6.9271,
        "longitude": 79.8612,
        "address": "Colombo General Hospital"
      },
      "status": "available",
      "capacity": {
        "patients": 2,
        "medical_crew": 3
      },
      "equipment": [
        "defibrillator",
        "oxygen_tank",
        "first_aid_kit"
      ],
      "availability_window": {
        "start": "2024-01-15T08:00:00Z",
        "end": "2024-01-15T20:00:00Z"
      },
      "contact": {
        "driver": "John Silva",
        "phone": "+94771234567"
      },
      "last_updated": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 25,
    "page": 1,
    "limit": 10,
    "pages": 3
  }
}
```

### Get Resource Details

```http
GET /api/resources/{resource_id}
```

Retrieve detailed information about a specific resource.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "resource_001",
    "type": "medical_team",
    "category": "personnel",
    "name": "Emergency Medical Team Alpha",
    "specialization": ["trauma", "pediatric", "cardiac"],
    "members": [
      {
        "id": "medic_001",
        "name": "Dr. Sarah Johnson",
        "role": "team_leader",
        "certifications": ["ACLS", "PALS", "ATLS"],
        "contact": "+94771234567"
      }
    ],
    "current_assignment": null,
    "deployment_history": [
      {
        "request_id": "req_456",
        "location": "Kandy District",
        "duration": "4 hours",
        "outcome": "successful"
      }
    ],
    "performance_metrics": {
      "response_time_avg": "12 minutes",
      "success_rate": 0.95,
      "availability_rate": 0.87
    }
  }
}
```

### Allocate Resource

```http
POST /api/resources/{resource_id}/allocate
```

Allocate a resource to an emergency request or task.

**Request Body:**
```json
{
  "request_id": "req_789",
  "task_id": "task_123",
  "allocated_by": "user_456",
  "allocation_type": "temporary",
  "duration_hours": 6,
  "priority": "high",
  "special_instructions": "Requires hazmat equipment"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "allocation_id": "alloc_001",
    "resource_id": "resource_001",
    "request_id": "req_789",
    "status": "allocated",
    "allocated_at": "2024-01-15T11:00:00Z",
    "estimated_completion": "2024-01-15T17:00:00Z",
    "allocation_details": {
      "contact_person": "John Silva",
      "contact_phone": "+94771234567",
      "deployment_location": {
        "latitude": 6.9271,
        "longitude": 79.8612
      }
    }
  }
}
```

### Update Resource Status

```http
PATCH /api/resources/{resource_id}
```

Update resource availability, location, or status.

**Request Body:**
```json
{
  "status": "maintenance",
  "location": {
    "latitude": 6.9271,
    "longitude": 79.8612
  },
  "maintenance_reason": "Scheduled inspection",
  "estimated_available": "2024-01-16T08:00:00Z"
}
```

### Resource Availability Forecast

```http
GET /api/resources/forecast
```

Get predicted resource availability for planning purposes.

**Query Parameters:**
- `location` (string, required): Target location for forecast
- `timeframe` (string, optional): Forecast period (1h, 6h, 24h, 7d)
- `resource_types` (array, optional): Specific resource types to forecast

**Response:**
```json
{
  "success": true,
  "data": {
    "location": "Colombo District",
    "timeframe": "24h",
    "forecast": [
      {
        "time": "2024-01-15T12:00:00Z",
        "available_resources": {
          "ambulances": 8,
          "fire_trucks": 4,
          "medical_teams": 12,
          "rescue_equipment": 15
        },
        "predicted_demand": {
          "ambulances": 3,
          "medical_teams": 5
        },
        "capacity_utilization": 0.35
      }
    ],
    "recommendations": [
      "Consider redistributing 2 ambulances from Gampaha to Colombo",
      "Medical team availability is sufficient for predicted demand"
    ]
  }
}
```

## Resource Types

### Vehicles
- **Ambulances**: Patient transport with medical equipment
- **Fire Trucks**: Fire suppression and rescue operations
- **Rescue Vehicles**: Specialized rescue equipment transport
- **Command Vehicles**: Mobile command centers

### Medical Supplies
- **Emergency Kits**: First aid and trauma supplies
- **Medications**: Emergency pharmaceuticals
- **Medical Equipment**: Portable medical devices
- **PPE**: Personal protective equipment

### Personnel
- **Medical Teams**: Doctors, nurses, paramedics
- **Rescue Teams**: Search and rescue specialists
- **Technical Teams**: Engineers, utility specialists
- **Support Staff**: Logistics and coordination personnel

### Equipment
- **Communication**: Radios, satellite phones
- **Search & Rescue**: Specialized rescue tools
- **Shelter**: Temporary housing materials
- **Power**: Generators, lighting equipment

## Real-time Updates

Resources support real-time status updates through WebSocket connections:

```javascript
// Subscribe to resource updates
const socket = new WebSocket('ws://localhost:8000/ws/resources');

socket.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log('Resource update:', update);
};

// Example update message
{
  "type": "resource_status_change",
  "resource_id": "resource_001",
  "old_status": "available",
  "new_status": "allocated",
  "timestamp": "2024-01-15T11:00:00Z",
  "allocation_details": {
    "request_id": "req_789",
    "estimated_duration": "6 hours"
  }
}
```

## Integration with AI Agents

Resources are automatically managed by AI agents for optimal allocation:

### Intelligent Allocation
- **Demand Prediction**: AI predicts resource needs based on historical data
- **Optimization**: Automatic resource allocation optimization
- **Rebalancing**: Dynamic resource redistribution

### Performance Monitoring
- **Utilization Tracking**: Monitor resource usage patterns
- **Efficiency Analysis**: Identify optimization opportunities
- **Predictive Maintenance**: Anticipate equipment maintenance needs

## Error Handling

Common error responses:

### Resource Not Found
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Resource with ID 'resource_001' not found",
    "details": {
      "resource_id": "resource_001"
    }
  }
}
```

### Resource Already Allocated
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_ALREADY_ALLOCATED",
    "message": "Resource is currently allocated to another request",
    "details": {
      "current_allocation": {
        "request_id": "req_456",
        "estimated_completion": "2024-01-15T16:00:00Z"
      }
    }
  }
}
```

### Insufficient Capacity
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_CAPACITY",
    "message": "Resource does not meet capacity requirements",
    "details": {
      "required_capacity": 5,
      "available_capacity": 2
    }
  }
}
```

## Best Practices

### Resource Management
- **Regular Updates**: Keep resource status current
- **Capacity Planning**: Maintain adequate resource reserves
- **Geographic Distribution**: Ensure resources are strategically located
- **Maintenance Scheduling**: Plan maintenance during low-demand periods

### Performance Optimization
- **Caching**: Cache frequently accessed resource data
- **Indexing**: Use location-based indexing for quick searches
- **Batch Operations**: Group resource updates when possible
- **Load Balancing**: Distribute resource queries across multiple servers

### Security Considerations
- **Access Control**: Restrict resource allocation to authorized users
- **Audit Logging**: Track all resource allocation changes
- **Data Validation**: Validate resource status updates
- **Rate Limiting**: Prevent abuse of resource APIs
