# Project Structure

This document outlines the organization and structure of the disaster response coordination web application.

## Overview

The project follows a modern full-stack architecture with clear separation of concerns:

```
disaster-response-app/
├── frontend/           # React TypeScript frontend
├── backend/           # FastAPI Python backend
├── ai_services/       # AI agents and MCP integration
├── docs/             # MkDocs documentation
├── docker/           # Docker configuration
└── README.md         # Project overview
```

## Frontend Structure (`/frontend`)

```
frontend/
├── public/                    # Static assets
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── common/          # Shared components
│   │   ├── dashboard/       # Dashboard components
│   │   ├── forms/           # Form components
│   │   └── WebSocketProvider.tsx
│   ├── pages/               # Page components by role
│   │   ├── FirstResponder/
│   │   ├── Volunteer/
│   │   ├── AffectedIndividual/
│   │   └── Government/
│   ├── hooks/               # Custom React hooks
│   ├── services/            # API and service layer
│   ├── types/               # TypeScript type definitions
│   ├── utils/               # Utility functions
│   ├── styles/              # Global styles and themes
│   ├── App.tsx              # Main application component
│   └── index.tsx            # Application entry point
├── package.json             # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
└── tailwind.config.js      # Tailwind CSS configuration
```

### Key Frontend Features

- **Role-based Routing**: Separate pages and components for each user role
- **Real-time Updates**: WebSocket integration for live coordination
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Type Safety**: Full TypeScript implementation
- **Component Library**: Reusable UI components with consistent styling

## Backend Structure (`/backend`)

```
backend/
├── app/
│   ├── api/                 # API route handlers
│   │   ├── v1/
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   ├── requests.py  # Emergency request management
│   │   │   ├── tasks.py     # Task coordination
│   │   │   ├── resources.py # Resource management
│   │   │   ├── users.py     # User management
│   │   │   └── websocket.py # WebSocket handlers
│   │   └── __init__.py
│   ├── core/                # Core application logic
│   │   ├── config.py        # Configuration management
│   │   ├── security.py      # Authentication & authorization
│   │   ├── database.py      # Database connection
│   │   └── websocket_manager.py
│   ├── models/              # Database models
│   │   ├── user.py
│   │   ├── request.py
│   │   ├── task.py
│   │   └── resource.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py
│   │   ├── request.py
│   │   ├── task.py
│   │   └── resource.py
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py
│   │   ├── request_service.py
│   │   ├── task_service.py
│   │   └── ai_service.py
│   └── main.py              # FastAPI application
├── tests/                   # Test suite
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── requirements.txt         # Python dependencies
└── alembic/                # Database migrations
```

### Key Backend Features

- **FastAPI Framework**: Modern, fast Python web framework
- **SQLAlchemy ORM**: Database abstraction and modeling
- **Pydantic Validation**: Request/response data validation
- **JWT Authentication**: Secure token-based authentication
- **WebSocket Support**: Real-time bidirectional communication
- **Role-based Access Control**: Granular permission system

## AI Services Structure (`/ai_services`)

```
ai_services/
├── agents/                  # AI agent implementations
│   ├── emergency_agent.py   # Emergency response coordination
│   ├── resource_agent.py    # Resource allocation optimization
│   ├── volunteer_agent.py   # Volunteer coordination
│   └── base_agent.py        # Base agent class
├── mcp_integration/         # Model Context Protocol
│   ├── server.py           # MCP server implementation
│   ├── tools.py            # MCP tool definitions
│   └── __init__.py
├── models/                  # AI model configurations
│   ├── llm_config.py       # Language model setup
│   └── embeddings.py       # Vector embedding models
├── utils/                   # AI utility functions
│   ├── text_processing.py
│   └── multimodal.py
├── run_mcp_server.py       # MCP server runner
└── requirements.txt        # AI service dependencies
```

### AI Services Features

- **Multi-Agent System**: Specialized agents for different coordination tasks
- **MCP Integration**: Standardized tool and resource access
- **Multimodal Processing**: Text, image, and audio input handling
- **Real-time Decision Making**: Intelligent task prioritization and assignment

## Documentation Structure (`/docs`)

```
docs/
├── index.md                 # Documentation homepage
├── getting-started/         # Setup and configuration
│   ├── quick-setup.md
│   ├── environment.md
│   └── docker.md
├── api/                     # API documentation
│   ├── authentication.md
│   ├── requests.md
│   ├── tasks.md
│   ├── resources.md
│   ├── users.md
│   ├── websocket.md
│   └── agents.md
├── user-guides/             # Role-based user guides
│   ├── affected-individuals.md
│   ├── volunteers.md
│   ├── first-responders.md
│   └── administrators.md
├── architecture/            # System architecture
│   ├── overview.md
│   ├── ai-agents.md
│   ├── database.md
│   └── api.md
├── development/             # Development guides
│   ├── structure.md         # This file
│   ├── testing.md
│   ├── contributing.md
│   └── deployment.md
├── mcp/                     # MCP documentation
│   ├── overview.md
│   ├── tools.md
│   └── setup.md
└── troubleshooting.md       # Common issues and solutions
```

## Configuration Files

### Frontend Configuration

- `package.json`: Dependencies, scripts, and project metadata
- `tsconfig.json`: TypeScript compiler configuration
- `tailwind.config.js`: Tailwind CSS customization
- `.env`: Environment variables for development

### Backend Configuration

- `requirements.txt`: Python package dependencies
- `alembic.ini`: Database migration configuration
- `.env`: Environment variables and secrets
- `pyproject.toml`: Python project configuration

### AI Services Configuration

- `requirements.txt`: AI-specific Python dependencies
- `config.yaml`: AI model and service configuration
- `.env`: API keys and model endpoints

## Development Workflow

1. **Frontend Development**: React components with TypeScript
2. **Backend Development**: FastAPI endpoints with automatic documentation
3. **AI Integration**: Agent development and MCP tool creation
4. **Testing**: Unit and integration tests across all layers
5. **Documentation**: MkDocs for comprehensive documentation
6. **Deployment**: Docker containers with orchestration

## Best Practices

- **Separation of Concerns**: Clear boundaries between layers
- **Type Safety**: TypeScript and Pydantic for type validation
- **Error Handling**: Comprehensive error handling across all services
- **Logging**: Structured logging for debugging and monitoring
- **Testing**: Automated testing at multiple levels
- **Documentation**: Living documentation that stays current with code
