# Users API

The Users API manages user accounts, profiles, roles, and permissions within the disaster response coordination system.

## Overview

The system supports multiple user roles with different capabilities:

- **Affected Individuals**: Submit emergency requests and track status
- **Volunteers**: Accept and complete response tasks
- **First Responders**: Professional emergency response personnel
- **Government Help Centre**: Administrative oversight and coordination

## Endpoints

### User Registration

```http
POST /api/users/register
```

Register a new user account with role-based capabilities.

**Request Body:**
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePassword123!",
  "firstName": "John",
  "lastName": "Doe",
  "phone": "+94771234567",
  "role": "volunteer",
  "profile": {
    "location": {
      "latitude": 6.9271,
      "longitude": 79.8612,
      "address": "Colombo, Sri Lanka"
    },
    "skills": ["first_aid", "search_rescue", "medical_assistance"],
    "availability": {
      "days": ["monday", "tuesday", "saturday", "sunday"],
      "hours": {
        "start": "09:00",
        "end": "17:00"
      }
    },
    "certifications": [
      {
        "name": "First Aid Certification",
        "issuer": "Red Cross",
        "expiry_date": "2025-06-15"
      }
    ],
    "emergency_contact": {
      "name": "Jane Doe",
      "phone": "+94771234568",
      "relationship": "spouse"
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "user_001",
    "email": "john.doe@example.com",
    "role": "volunteer",
    "status": "pending_verification",
    "created_at": "2024-01-15T10:30:00Z",
    "verification_token": "verify_abc123"
  },
  "message": "Registration successful. Please check your email for verification instructions."
}
```

### Get User Profile

```http
GET /api/users/profile
```

Get the authenticated user's profile information.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "user_001",
    "email": "john.doe@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "phone": "+94771234567",
    "role": "volunteer",
    "status": "active",
    "profile": {
      "location": {
        "latitude": 6.9271,
        "longitude": 79.8612,
        "address": "Colombo, Sri Lanka"
      },
      "skills": ["first_aid", "search_rescue", "medical_assistance"],
      "availability": {
        "status": "available",
        "next_available": "2024-01-15T12:00:00Z"
      },
      "performance_metrics": {
        "tasks_completed": 23,
        "success_rate": 0.96,
        "average_response_time": "15 minutes",
        "rating": 4.8
      },
      "certifications": [
        {
          "name": "First Aid Certification",
          "issuer": "Red Cross",
          "status": "valid",
          "expiry_date": "2025-06-15"
        }
      ]
    },
    "settings": {
      "notifications": {
        "email": true,
        "sms": true,
        "push": true
      },
      "privacy": {
        "location_sharing": "emergency_only",
        "profile_visibility": "volunteers_only"
      }
    },
    "created_at": "2024-01-15T10:30:00Z",
    "last_active": "2024-01-15T11:45:00Z"
  }
}
```

### Update User Profile

```http
PATCH /api/users/profile
```

Update user profile information and settings.

**Request Body:**
```json
{
  "phone": "+94771234569",
  "profile": {
    "skills": ["first_aid", "search_rescue", "medical_assistance", "translation"],
    "availability": {
      "days": ["monday", "tuesday", "wednesday", "saturday", "sunday"],
      "hours": {
        "start": "08:00",
        "end": "18:00"
      }
    }
  },
  "settings": {
    "notifications": {
      "email": true,
      "sms": false,
      "push": true
    }
  }
}
```

### List Users (Admin Only)

```http
GET /api/users
```

List all users with filtering and pagination options.

**Query Parameters:**
- `role` (string, optional): Filter by user role
- `status` (string, optional): Filter by user status (active, inactive, pending)
- `location` (string, optional): Filter by location area
- `skills` (array, optional): Filter by required skills
- `page` (number, optional): Page number for pagination
- `limit` (number, optional): Number of users per page

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "user_001",
      "email": "john.doe@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "volunteer",
      "status": "active",
      "location": "Colombo, Sri Lanka",
      "skills": ["first_aid", "search_rescue"],
      "availability": "available",
      "performance": {
        "tasks_completed": 23,
        "rating": 4.8
      },
      "last_active": "2024-01-15T11:45:00Z"
    }
  ],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "pages": 8
  }
}
```

### User Verification

```http
POST /api/users/verify
```

Verify user email address or credentials.

**Request Body:**
```json
{
  "token": "verify_abc123",
  "type": "email"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email verification successful",
  "data": {
    "user_id": "user_001",
    "status": "active",
    "verified_at": "2024-01-15T12:00:00Z"
  }
}
```

### Change User Status

```http
PATCH /api/users/{user_id}/status
```

Update user account status (admin only).

**Request Body:**
```json
{
  "status": "suspended",
  "reason": "Policy violation",
  "notes": "Temporary suspension pending review"
}
```

### User Activity History

```http
GET /api/users/{user_id}/activity
```

Get user activity and task history.

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "user_001",
    "activity_summary": {
      "total_tasks": 23,
      "completed_tasks": 22,
      "cancelled_tasks": 1,
      "average_completion_time": "2.5 hours",
      "total_hours_contributed": 58.5
    },
    "recent_activities": [
      {
        "id": "activity_001",
        "type": "task_completed",
        "task_id": "task_456",
        "title": "Medical assistance - Kandy",
        "completion_time": "2.2 hours",
        "rating_received": 5,
        "timestamp": "2024-01-14T16:30:00Z"
      },
      {
        "id": "activity_002",
        "type": "task_accepted",
        "task_id": "task_789",
        "title": "Supply distribution - Galle",
        "accepted_at": "2024-01-15T09:00:00Z"
      }
    ],
    "performance_trends": {
      "response_time_trend": "improving",
      "completion_rate_trend": "stable",
      "rating_trend": "improving"
    }
  }
}
```

## Role-Based Features

### Affected Individuals
- **Emergency Requests**: Submit and track emergency requests
- **Status Updates**: Receive real-time updates on assistance
- **Resource Information**: Access available resources in their area
- **Communication**: Direct communication with assigned responders

### Volunteers
- **Task Management**: Browse, accept, and complete tasks
- **Skill Matching**: Receive tasks matching their skills
- **Availability Management**: Set availability schedules
- **Performance Tracking**: View task completion metrics

### First Responders
- **Professional Dashboard**: Advanced coordination tools
- **Resource Management**: Access to resource allocation
- **Team Coordination**: Collaborate with other responders
- **Incident Command**: Lead response operations

### Government Help Centre
- **System Administration**: User management and oversight
- **Analytics Dashboard**: System-wide performance metrics
- **Policy Management**: Configure system policies
- **Audit Trails**: Access comprehensive system logs

## User Status Types

### Account Status
- **active**: Full system access
- **inactive**: Limited access, can reactivate
- **suspended**: Temporary restriction
- **banned**: Permanent restriction
- **pending_verification**: Awaiting email/credential verification

### Availability Status (Volunteers/Responders)
- **available**: Ready to accept tasks
- **busy**: Currently assigned to tasks
- **unavailable**: Temporarily not available
- **off_duty**: Scheduled break or end of shift

## Notification Preferences

Users can configure notification settings:

```json
{
  "notifications": {
    "email": {
      "enabled": true,
      "types": ["task_assignment", "emergency_updates", "system_alerts"]
    },
    "sms": {
      "enabled": true,
      "types": ["urgent_tasks", "emergency_alerts"]
    },
    "push": {
      "enabled": true,
      "types": ["all"]
    },
    "frequency": {
      "digest": "daily",
      "real_time": ["urgent", "emergency"]
    }
  }
}
```

## Privacy and Security

### Data Protection
- **Personal Information**: Secure storage and limited sharing
- **Location Privacy**: Configurable location sharing settings
- **Communication Privacy**: Encrypted messaging
- **Data Retention**: Configurable data retention policies

### Access Control
- **Role-Based Permissions**: Fine-grained access control
- **API Rate Limiting**: Prevent abuse
- **Session Management**: Secure session handling
- **Audit Logging**: Comprehensive activity tracking

## Error Handling

### User Not Found
```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 'user_001' not found"
  }
}
```

### Insufficient Permissions
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_PERMISSIONS",
    "message": "User does not have permission to perform this action",
    "details": {
      "required_role": "government_admin",
      "user_role": "volunteer"
    }
  }
}
```

### Validation Errors
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": "Invalid email format",
      "phone": "Phone number is required"
    }
  }
}
```

## Integration Examples

### User Registration Flow
```javascript
// Register new volunteer
const registerUser = async (userData) => {
  try {
    const response = await fetch('/api/users/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData)
    });
    
    const result = await response.json();
    
    if (result.success) {
      // Redirect to verification page
      window.location.href = `/verify?token=${result.data.verification_token}`;
    }
  } catch (error) {
    console.error('Registration failed:', error);
  }
};
```

### Profile Management
```javascript
// Update user availability
const updateAvailability = async (availability) => {
  const token = localStorage.getItem('auth_token');
  
  const response = await fetch('/api/users/profile', {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      profile: { availability }
    })
  });
  
  return response.json();
};
```

## Best Practices

### User Management
- **Regular Verification**: Periodic credential verification
- **Performance Monitoring**: Track user engagement and performance
- **Feedback Collection**: Gather user feedback for improvements
- **Training Programs**: Provide ongoing user training

### Security Best Practices
- **Strong Authentication**: Enforce strong password policies
- **Regular Audits**: Monitor user activity for suspicious behavior
- **Data Minimization**: Collect only necessary user information
- **Secure Communications**: Use encrypted channels for sensitive data
