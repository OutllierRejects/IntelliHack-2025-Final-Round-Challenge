# API Architecture

This document describes the API architecture for the disaster response coordination system, including design principles, endpoint organization, security implementation, and integration patterns.

## API Design Philosophy

### RESTful Design Principles

The API follows REST architectural principles with some extensions for real-time capabilities:

- **Resource-Based URLs**: Clear resource identification in URLs
- **HTTP Methods**: Proper use of GET, POST, PUT, PATCH, DELETE
- **Stateless Communication**: Each request contains all necessary information
- **Cacheable Responses**: Appropriate cache headers and strategies
- **Layered System**: Clean separation between client and server

### API Versioning Strategy

```
Base URL: https://api.disaster-response.com/v1/
Versioning: URL-based versioning (/v1/, /v2/, etc.)
Deprecation: 12-month deprecation policy for major versions
```

## API Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Application]
        MOBILE[Mobile App]
        THIRD_PARTY[Third-party Clients]
    end

    subgraph "API Gateway Layer"
        GATEWAY[API Gateway]
        RATE_LIMIT[Rate Limiting]
        AUTH[Authentication]
        TRANSFORM[Request/Response Transform]
        CACHE[Response Cache]
    end

    subgraph "API Services"
        USER_API[User Service API]
        REQUEST_API[Request Service API]
        TASK_API[Task Service API]
        RESOURCE_API[Resource Service API]
        NOTIFICATION_API[Notification Service API]
        AI_API[AI Agent Service API]
    end

    subgraph "Business Logic Layer"
        USER_BL[User Business Logic]
        REQUEST_BL[Request Business Logic]
        TASK_BL[Task Business Logic]
        RESOURCE_BL[Resource Business Logic]
        NOTIFICATION_BL[Notification Business Logic]
        AI_BL[AI Agent Business Logic]
    end

    subgraph "Data Access Layer"
        USER_DAL[User Data Access]
        REQUEST_DAL[Request Data Access]
        TASK_DAL[Task Data Access]
        RESOURCE_DAL[Resource Data Access]
        NOTIFICATION_DAL[Notification Data Access]
        AI_DAL[AI Data Access]
    end

    subgraph "Data Layer"
        POSTGRES[(PostgreSQL)]
        REDIS[(Redis Cache)]
        SEARCH[(Elasticsearch)]
    end

    WEB --> GATEWAY
    MOBILE --> GATEWAY
    THIRD_PARTY --> GATEWAY

    GATEWAY --> RATE_LIMIT
    RATE_LIMIT --> AUTH
    AUTH --> TRANSFORM
    TRANSFORM --> CACHE

    CACHE --> USER_API
    CACHE --> REQUEST_API
    CACHE --> TASK_API
    CACHE --> RESOURCE_API
    CACHE --> NOTIFICATION_API
    CACHE --> AI_API

    USER_API --> USER_BL --> USER_DAL
    REQUEST_API --> REQUEST_BL --> REQUEST_DAL
    TASK_API --> TASK_BL --> TASK_DAL
    RESOURCE_API --> RESOURCE_BL --> RESOURCE_DAL
    NOTIFICATION_API --> NOTIFICATION_BL --> NOTIFICATION_DAL
    AI_API --> AI_BL --> AI_DAL

    USER_DAL --> POSTGRES
    REQUEST_DAL --> POSTGRES
    TASK_DAL --> POSTGRES
    RESOURCE_DAL --> POSTGRES
    NOTIFICATION_DAL --> POSTGRES
    AI_DAL --> POSTGRES

    USER_DAL --> REDIS
    REQUEST_DAL --> REDIS
    TASK_DAL --> SEARCH
```

## API Service Structure

### Core API Services

#### 1. User Service API

```
Base Path: /api/v1/users

Endpoints:
├── POST   /register           # User registration
├── POST   /login              # User authentication
├── POST   /logout             # User logout
├── GET    /profile            # Get user profile
├── PATCH  /profile            # Update user profile
├── POST   /verify             # Email verification
├── POST   /forgot-password    # Password reset request
├── POST   /reset-password     # Password reset
├── GET    /{id}               # Get user by ID (admin)
├── GET    /                   # List users (admin)
├── PATCH  /{id}/status        # Update user status (admin)
└── GET    /{id}/activity      # User activity history
```

#### 2. Emergency Requests Service API

```
Base Path: /api/v1/requests

Endpoints:
├── POST   /                   # Create emergency request
├── GET    /                   # List emergency requests
├── GET    /{id}               # Get request details
├── PATCH  /{id}               # Update request
├── DELETE /{id}               # Cancel request
├── POST   /{id}/assign        # Assign responders
├── GET    /{id}/tasks         # Get related tasks
├── GET    /{id}/resources     # Get allocated resources
├── POST   /{id}/comments      # Add comment/update
├── GET    /nearby             # Get nearby requests
├── GET    /statistics         # Request statistics
└── POST   /{id}/media         # Upload media files
```

#### 3. Task Management Service API

```
Base Path: /api/v1/tasks

Endpoints:
├── POST   /                   # Create task
├── GET    /                   # List tasks
├── GET    /{id}               # Get task details
├── PATCH  /{id}               # Update task
├── DELETE /{id}               # Cancel task
├── POST   /{id}/accept        # Accept task
├── POST   /{id}/complete      # Complete task
├── POST   /{id}/rate          # Rate task completion
├── GET    /my-tasks           # Get user's tasks
├── GET    /available          # Get available tasks
└── GET    /{id}/history       # Task history
```

#### 4. Resource Management Service API

```
Base Path: /api/v1/resources

Endpoints:
├── GET    /                   # List resources
├── GET    /{id}               # Get resource details
├── PATCH  /{id}               # Update resource
├── POST   /{id}/allocate      # Allocate resource
├── POST   /{id}/deallocate    # Deallocate resource
├── GET    /available          # Get available resources
├── GET    /forecast           # Resource availability forecast
├── GET    /types              # Get resource types
├── GET    /nearby             # Get nearby resources
└── GET    /statistics         # Resource statistics
```

#### 5. Notification Service API

```
Base Path: /api/v1/notifications

Endpoints:
├── POST   /                   # Send notification
├── GET    /                   # List notifications
├── GET    /{id}               # Get notification details
├── PATCH  /{id}/read          # Mark as read
├── DELETE /{id}               # Delete notification
├── POST   /batch              # Send batch notifications
├── GET    /unread             # Get unread notifications
├── PATCH  /mark-all-read      # Mark all as read
└── GET    /preferences        # Get notification preferences
```

#### 6. AI Agent Service API

```
Base Path: /api/v1/ai-agents

Endpoints:
├── POST   /emergency-processor/analyze    # Analyze emergency
├── POST   /resource-optimizer/optimize    # Optimize resources
├── POST   /coordinator/assign-tasks       # Assign tasks
├── POST   /predictor/forecast             # Generate predictions
├── POST   /communicator/send-notifications # Send notifications
├── GET    /status                         # Get agent status
├── GET    /{agent}/metrics               # Get agent metrics
├── POST   /feedback                      # Submit feedback
└── POST   /{agent}/retrain               # Retrain agent
```

## API Request/Response Patterns

### Standard Request Format

#### Authentication Header

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Content Type

```http
Content-Type: application/json
Accept: application/json
```

#### Request Body Structure

```json
{
  "data": {
    // Primary request data
  },
  "metadata": {
    "client_version": "1.2.0",
    "client_platform": "web",
    "request_id": "req_12345"
  }
}
```

### Standard Response Format

#### Success Response

```json
{
  "success": true,
  "data": {
    // Response data
  },
  "metadata": {
    "timestamp": "2024-01-15T12:00:00Z",
    "request_id": "req_12345",
    "processing_time_ms": 150
  },
  "pagination": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    },
    "trace_id": "trace_12345"
  },
  "metadata": {
    "timestamp": "2024-01-15T12:00:00Z",
    "request_id": "req_12345"
  }
}
```

## Authentication and Authorization

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_12345",
    "email": "user@example.com",
    "role": "volunteer",
    "permissions": ["task_read", "task_write", "request_read"],
    "iat": 1705315200,
    "exp": 1705401600,
    "iss": "disaster-response-api"
  }
}
```

### Role-Based Access Control

```typescript
interface UserPermissions {
  affected_individual: [
    "request_create",
    "request_read_own",
    "request_update_own",
    "notification_read_own"
  ];
  volunteer: [
    "request_read",
    "task_read",
    "task_accept",
    "task_complete",
    "resource_read",
    "notification_read_own"
  ];
  first_responder: [
    "request_read",
    "request_assign",
    "task_read",
    "task_create",
    "task_assign",
    "resource_read",
    "resource_allocate",
    "notification_send"
  ];
  government_admin: [
    "user_read",
    "user_manage",
    "request_read_all",
    "task_read_all",
    "resource_read_all",
    "resource_manage",
    "notification_send_all",
    "analytics_read"
  ];
}
```

### Authorization Middleware

```typescript
import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";

interface AuthenticatedRequest extends Request {
  user?: {
    id: string;
    email: string;
    role: string;
    permissions: string[];
  };
}

export const authenticate = (
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
) => {
  try {
    const token = req.header("Authorization")?.replace("Bearer ", "");

    if (!token) {
      return res.status(401).json({
        success: false,
        error: {
          code: "MISSING_TOKEN",
          message: "Access token is required",
        },
      });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({
      success: false,
      error: {
        code: "INVALID_TOKEN",
        message: "Invalid or expired token",
      },
    });
  }
};

export const authorize = (requiredPermission: string) => {
  return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    if (!req.user?.permissions.includes(requiredPermission)) {
      return res.status(403).json({
        success: false,
        error: {
          code: "INSUFFICIENT_PERMISSIONS",
          message: "Insufficient permissions for this action",
          details: {
            required: requiredPermission,
            user_permissions: req.user?.permissions || [],
          },
        },
      });
    }
    next();
  };
};
```

## API Gateway Implementation

### Rate Limiting Strategy

```typescript
import rateLimit from "express-rate-limit";
import RedisStore from "rate-limit-redis";
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL);

// Different rate limits for different user types
const createRateLimiter = (
  windowMs: number,
  max: number,
  keyGenerator?: (req: Request) => string
) => {
  return rateLimit({
    store: new RedisStore({
      client: redis,
      prefix: "rl:",
    }),
    windowMs,
    max,
    keyGenerator: keyGenerator || ((req) => req.ip),
    message: {
      success: false,
      error: {
        code: "RATE_LIMIT_EXCEEDED",
        message: "Too many requests, please try again later",
      },
    },
  });
};

// Apply different limits based on user role
export const dynamicRateLimit = (
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
) => {
  const userRole = req.user?.role || "anonymous";

  const limits = {
    anonymous: createRateLimiter(15 * 60 * 1000, 100), // 100 requests per 15 minutes
    affected_individual: createRateLimiter(15 * 60 * 1000, 200),
    volunteer: createRateLimiter(15 * 60 * 1000, 500),
    first_responder: createRateLimiter(15 * 60 * 1000, 1000),
    government_admin: createRateLimiter(15 * 60 * 1000, 2000),
  };

  const limiter = limits[userRole] || limits.anonymous;
  limiter(req, res, next);
};
```

### Request Validation

```typescript
import Joi from "joi";
import { Request, Response, NextFunction } from "express";

export const validateRequest = (schema: Joi.ObjectSchema) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true,
    });

    if (error) {
      const validationErrors = error.details.map((detail) => ({
        field: detail.path.join("."),
        message: detail.message,
        value: detail.context?.value,
      }));

      return res.status(400).json({
        success: false,
        error: {
          code: "VALIDATION_ERROR",
          message: "Request validation failed",
          details: validationErrors,
        },
      });
    }

    req.body = value;
    next();
  };
};

// Example validation schema
export const createEmergencyRequestSchema = Joi.object({
  title: Joi.string().required().min(10).max(255),
  description: Joi.string().required().min(20).max(2000),
  category: Joi.string()
    .valid(
      "medical",
      "fire",
      "natural_disaster",
      "accident",
      "security",
      "utility_failure",
      "other"
    )
    .required(),
  severity: Joi.string().valid("low", "medium", "high", "critical").required(),
  location: Joi.object({
    latitude: Joi.number().min(-90).max(90).required(),
    longitude: Joi.number().min(-180).max(180).required(),
    address: Joi.string().max(500),
  }).required(),
  contact_info: Joi.object({
    phone: Joi.string().pattern(/^\+[1-9]\d{1,14}$/),
    email: Joi.string().email(),
    name: Joi.string().max(100),
  }),
  media_urls: Joi.array().items(Joi.string().uri()).max(10),
});
```

## Caching Strategy

### Multi-Layer Caching

```typescript
import Redis from "ioredis";
import { Request, Response, NextFunction } from "express";

const redis = new Redis(process.env.REDIS_URL);

// Cache middleware
export const cacheResponse = (ttl: number = 300, keyPrefix: string = "api") => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const cacheKey = `${keyPrefix}:${req.method}:${req.path}:${JSON.stringify(
      req.query
    )}`;

    try {
      const cachedResponse = await redis.get(cacheKey);

      if (cachedResponse) {
        const parsed = JSON.parse(cachedResponse);
        return res.json({
          ...parsed,
          metadata: {
            ...parsed.metadata,
            cached: true,
            cache_age: Date.now() - parsed.metadata.timestamp,
          },
        });
      }

      // Store original res.json function
      const originalJson = res.json;

      // Override res.json to cache the response
      res.json = function (body: any) {
        // Cache successful responses only
        if (body.success !== false) {
          redis.setex(cacheKey, ttl, JSON.stringify(body));
        }

        // Call original function
        return originalJson.call(this, body);
      };

      next();
    } catch (error) {
      // If cache fails, continue without caching
      next();
    }
  };
};

// Cache invalidation
export const invalidateCache = async (pattern: string) => {
  const keys = await redis.keys(pattern);
  if (keys.length > 0) {
    await redis.del(...keys);
  }
};
```

### Cache Headers

```typescript
export const setCacheHeaders = (maxAge: number = 300) => {
  return (req: Request, res: Response, next: NextFunction) => {
    res.set({
      "Cache-Control": `public, max-age=${maxAge}`,
      ETag: `"${Date.now()}"`,
      "Last-Modified": new Date().toUTCString(),
    });
    next();
  };
};
```

## Real-time API Features

### WebSocket Integration

```typescript
import { Server as SocketIOServer } from "socket.io";
import { authenticate as authenticateWebSocket } from "../middleware/auth";

export class WebSocketService {
  private io: SocketIOServer;
  private userSockets: Map<string, string[]> = new Map();

  constructor(io: SocketIOServer) {
    this.io = io;
    this.setupMiddleware();
    this.setupEventHandlers();
  }

  private setupMiddleware() {
    this.io.use(authenticateWebSocket);
  }

  private setupEventHandlers() {
    this.io.on("connection", (socket) => {
      const userId = socket.data.user.id;

      // Track user connections
      const userConnections = this.userSockets.get(userId) || [];
      userConnections.push(socket.id);
      this.userSockets.set(userId, userConnections);

      // Handle subscriptions
      socket.on("subscribe", (channels: string[]) => {
        channels.forEach((channel) => {
          if (this.canSubscribeToChannel(socket.data.user, channel)) {
            socket.join(channel);
          }
        });
      });

      // Handle disconnection
      socket.on("disconnect", () => {
        const userConnections = this.userSockets.get(userId) || [];
        const updatedConnections = userConnections.filter(
          (id) => id !== socket.id
        );

        if (updatedConnections.length === 0) {
          this.userSockets.delete(userId);
        } else {
          this.userSockets.set(userId, updatedConnections);
        }
      });
    });
  }

  private canSubscribeToChannel(user: any, channel: string): boolean {
    const channelPermissions = {
      emergency_alerts: ["volunteer", "first_responder", "government_admin"],
      task_updates: ["volunteer", "first_responder", "government_admin"],
      resource_changes: ["first_responder", "government_admin"],
      system_alerts: ["government_admin"],
    };

    return channelPermissions[channel]?.includes(user.role) || false;
  }

  public broadcastToChannel(channel: string, data: any) {
    this.io.to(channel).emit("message", data);
  }

  public sendToUser(userId: string, data: any) {
    const userConnections = this.userSockets.get(userId) || [];
    userConnections.forEach((socketId) => {
      this.io.to(socketId).emit("message", data);
    });
  }
}
```

### Server-Sent Events (SSE)

```typescript
import { Request, Response } from "express";
import { EventEmitter } from "events";

class SSEService extends EventEmitter {
  private connections: Map<string, Response[]> = new Map();

  public addConnection(userId: string, res: Response) {
    const userConnections = this.connections.get(userId) || [];
    userConnections.push(res);
    this.connections.set(userId, userConnections);

    // Setup SSE headers
    res.writeHead(200, {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Cache-Control",
    });

    // Send initial connection message
    res.write(
      `data: ${JSON.stringify({
        type: "connected",
        timestamp: new Date().toISOString(),
      })}\n\n`
    );

    // Handle connection close
    res.on("close", () => {
      this.removeConnection(userId, res);
    });
  }

  private removeConnection(userId: string, res: Response) {
    const userConnections = this.connections.get(userId) || [];
    const updatedConnections = userConnections.filter((conn) => conn !== res);

    if (updatedConnections.length === 0) {
      this.connections.delete(userId);
    } else {
      this.connections.set(userId, updatedConnections);
    }
  }

  public sendEventToUser(userId: string, event: string, data: any) {
    const userConnections = this.connections.get(userId) || [];
    const message = `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;

    userConnections.forEach((res) => {
      try {
        res.write(message);
      } catch (error) {
        this.removeConnection(userId, res);
      }
    });
  }

  public broadcastEvent(event: string, data: any) {
    const message = `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;

    this.connections.forEach((connections, userId) => {
      connections.forEach((res) => {
        try {
          res.write(message);
        } catch (error) {
          this.removeConnection(userId, res);
        }
      });
    });
  }
}

export const sseService = new SSEService();

export const sseEndpoint = (req: AuthenticatedRequest, res: Response) => {
  const userId = req.user!.id;
  sseService.addConnection(userId, res);
};
```

## API Documentation

### OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: Disaster Response Coordination API
  description: API for disaster response coordination system
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@disaster-response.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.disaster-response.com/v1
    description: Production server
  - url: https://staging-api.disaster-response.com/v1
    description: Staging server

security:
  - BearerAuth: []

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    EmergencyRequest:
      type: object
      required:
        - title
        - description
        - category
        - severity
        - location
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        title:
          type: string
          minLength: 10
          maxLength: 255
        description:
          type: string
          minLength: 20
          maxLength: 2000
        category:
          type: string
          enum:
            [
              medical,
              fire,
              natural_disaster,
              accident,
              security,
              utility_failure,
              other,
            ]
        severity:
          type: string
          enum: [low, medium, high, critical]
        location:
          $ref: "#/components/schemas/Location"

    Location:
      type: object
      required:
        - latitude
        - longitude
      properties:
        latitude:
          type: number
          minimum: -90
          maximum: 90
        longitude:
          type: number
          minimum: -180
          maximum: 180
        address:
          type: string
          maxLength: 500

paths:
  /requests:
    post:
      summary: Create emergency request
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/EmergencyRequest"
      responses:
        "201":
          description: Emergency request created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    $ref: "#/components/schemas/EmergencyRequest"
```

## Error Handling

### Global Error Handler

```typescript
import { Request, Response, NextFunction } from "express";
import { ValidationError } from "joi";
import { JsonWebTokenError } from "jsonwebtoken";

export interface ApiError extends Error {
  statusCode?: number;
  code?: string;
  details?: any;
}

export const globalErrorHandler = (
  error: ApiError,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  let statusCode = error.statusCode || 500;
  let errorCode = error.code || "INTERNAL_SERVER_ERROR";
  let message = error.message || "An unexpected error occurred";
  let details = error.details || null;

  // Handle specific error types
  if (error instanceof ValidationError) {
    statusCode = 400;
    errorCode = "VALIDATION_ERROR";
    details = error.details.map((detail) => ({
      field: detail.path.join("."),
      message: detail.message,
    }));
  } else if (error instanceof JsonWebTokenError) {
    statusCode = 401;
    errorCode = "AUTHENTICATION_ERROR";
    message = "Invalid or expired token";
  }

  // Log error for monitoring
  console.error("API Error:", {
    statusCode,
    errorCode,
    message,
    details,
    stack: error.stack,
    url: req.url,
    method: req.method,
    userId: (req as any).user?.id,
  });

  res.status(statusCode).json({
    success: false,
    error: {
      code: errorCode,
      message,
      details,
      trace_id: req.headers["x-trace-id"] || "unknown",
    },
    metadata: {
      timestamp: new Date().toISOString(),
      request_id: req.headers["x-request-id"] || "unknown",
    },
  });
};
```

## API Performance Monitoring

### Response Time Middleware

```typescript
import { Request, Response, NextFunction } from "express";

export const responseTimeMiddleware = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const startTime = Date.now();

  // Override res.json to capture response time
  const originalJson = res.json;
  res.json = function (body: any) {
    const responseTime = Date.now() - startTime;

    // Add response time to metadata
    if (body && typeof body === "object" && body.metadata) {
      body.metadata.processing_time_ms = responseTime;
    }

    // Log slow requests
    if (responseTime > 1000) {
      console.warn("Slow API request:", {
        url: req.url,
        method: req.method,
        responseTime,
        userId: (req as any).user?.id,
      });
    }

    return originalJson.call(this, body);
  };

  next();
};
```

### Health Check Endpoints

```typescript
import { Request, Response } from "express";
import { Pool } from "pg";
import Redis from "ioredis";

const db = new Pool({ connectionString: process.env.DATABASE_URL });
const redis = new Redis(process.env.REDIS_URL);

export const healthCheck = async (req: Request, res: Response) => {
  const startTime = Date.now();
  const checks = {
    database: false,
    redis: false,
    external_services: false,
  };

  try {
    // Database health check
    await db.query("SELECT 1");
    checks.database = true;
  } catch (error) {
    console.error("Database health check failed:", error);
  }

  try {
    // Redis health check
    await redis.ping();
    checks.redis = true;
  } catch (error) {
    console.error("Redis health check failed:", error);
  }

  try {
    // External services health check
    // Add checks for critical external services
    checks.external_services = true;
  } catch (error) {
    console.error("External services health check failed:", error);
  }

  const isHealthy = Object.values(checks).every((check) => check);
  const responseTime = Date.now() - startTime;

  res.status(isHealthy ? 200 : 503).json({
    status: isHealthy ? "healthy" : "unhealthy",
    timestamp: new Date().toISOString(),
    response_time_ms: responseTime,
    checks,
    version: process.env.API_VERSION || "1.0.0",
    uptime: process.uptime(),
  });
};
```

## API Testing Strategy

### Unit Tests

```typescript
import request from "supertest";
import { app } from "../app";
import { createTestUser, generateJWT } from "../utils/test-helpers";

describe("Emergency Requests API", () => {
  let userToken: string;
  let userId: string;

  beforeEach(async () => {
    const user = await createTestUser({ role: "affected_individual" });
    userId = user.id;
    userToken = generateJWT(user);
  });

  describe("POST /api/v1/requests", () => {
    it("should create emergency request with valid data", async () => {
      const requestData = {
        title: "Medical emergency - chest pain",
        description: "Experiencing severe chest pain and shortness of breath",
        category: "medical",
        severity: "high",
        location: {
          latitude: 6.9271,
          longitude: 79.8612,
          address: "123 Main Street, Colombo",
        },
      };

      const response = await request(app)
        .post("/api/v1/requests")
        .set("Authorization", `Bearer ${userToken}`)
        .send(requestData)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.title).toBe(requestData.title);
      expect(response.body.data.user_id).toBe(userId);
    });

    it("should return validation error for invalid data", async () => {
      const invalidData = {
        title: "Short", // Too short
        description: "Short description", // Too short
        category: "invalid_category", // Invalid category
        severity: "high",
        location: {
          latitude: 200, // Invalid latitude
          longitude: 79.8612,
        },
      };

      const response = await request(app)
        .post("/api/v1/requests")
        .set("Authorization", `Bearer ${userToken}`)
        .send(invalidData)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe("VALIDATION_ERROR");
    });
  });
});
```

### Integration Tests

```typescript
describe("Emergency Request Workflow Integration", () => {
  it("should complete full emergency request workflow", async () => {
    // 1. Create emergency request
    const request = await createEmergencyRequest();

    // 2. AI agent should analyze request
    await waitForAIAnalysis(request.id);

    // 3. Tasks should be created
    const tasks = await getTasks(request.id);
    expect(tasks.length).toBeGreaterThan(0);

    // 4. Resources should be allocated
    const resources = await getResources(request.id);
    expect(resources.length).toBeGreaterThan(0);

    // 5. Notifications should be sent
    const notifications = await getNotifications(request.id);
    expect(notifications.length).toBeGreaterThan(0);
  });
});
```

## API Deployment Considerations

### Environment Configuration

```typescript
export const config = {
  port: process.env.PORT || 3000,
  database: {
    url: process.env.DATABASE_URL!,
    pool: {
      min: parseInt(process.env.DB_POOL_MIN || "2"),
      max: parseInt(process.env.DB_POOL_MAX || "10"),
    },
  },
  redis: {
    url: process.env.REDIS_URL!,
    retryDelayOnFailover: 100,
    maxRetriesPerRequest: 3,
  },
  jwt: {
    secret: process.env.JWT_SECRET!,
    expiresIn: process.env.JWT_EXPIRES_IN || "24h",
  },
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW || "900000"), // 15 minutes
    max: parseInt(process.env.RATE_LIMIT_MAX || "100"),
  },
  cors: {
    origin: process.env.CORS_ORIGIN?.split(",") || ["http://localhost:3000"],
    credentials: true,
  },
};
```

### Container Deployment

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

USER node

EXPOSE 3000

CMD ["npm", "start"]
```

This comprehensive API architecture provides a robust foundation for the disaster response coordination system with proper authentication, caching, real-time features, error handling, and monitoring capabilities.
