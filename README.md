# Disaster Response Coordination System

A comprehensive disaster response management system featuring AI-powered multi-agent coordination, real-time communication, and role-based dashboards for emergency response teams.

## 🚀 Features

### Core Functionality
- **AI-Powered Agent Workflow**: Automated disaster request processing through Intake → Prioritization → Assignment → Communication agents
- **Real-time Coordination**: WebSocket-based live updates and notifications
- **Role-based Dashboards**: Specialized interfaces for Affected Individuals, Volunteers, First Responders, and Administrators
- **Resource Management**: Track and manage emergency supplies, equipment, and personnel
- **Task Assignment**: Intelligent task distribution and tracking system
- **Multi-channel Communication**: SMS, email, and in-app notifications

### Technology Stack
- **Frontend**: React 19 + TypeScript, Tailwind CSS, React Router, React Query, Zustand
- **Backend**: FastAPI (Python), PostgreSQL, Redis, WebSockets
- **AI Agents**: AGNO framework with OpenAI GPT-4o-mini models
- **Infrastructure**: Docker, Docker Compose, Nginx, Traefik
- **Monitoring**: Flower (Celery), pgAdmin, Redis Commander

## 🛠 Quick Setup

### Prerequisites
- Docker and Docker Compose
- Git
- Make (for convenience commands)

### 1. Clone and Environment Setup

```bash
git clone <repository-url>
cd IntelliHack-2025-Final-Round-Challenge

# Copy and configure environment variables
cp ai_services/.env.example ai_services/.env
```

### 2. Configure Environment Variables

Edit `ai_services/.env` with your settings:

```env
# Database Configuration
DATABASE_URL=postgresql://disaster_user:disaster_pass@postgres:5432/disaster_response
POSTGRES_USER=disaster_user
POSTGRES_PASSWORD=disaster_pass
POSTGRES_DB=disaster_response

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration (Required for AI Agents)
OPENAI_API_KEY=your-openai-api-key-here

# SMS/Email Configuration (Optional)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-email-password

# Environment
ENVIRONMENT=development
DEBUG=true
```

### 3. Start the System

```bash
# Build and start all services
make docker-up

# Or manually with Docker Compose
docker-compose up --build
```

### 4. Initialize Database and Sample Data

```bash
# Run database migrations and load sample data
make db-migrate
make db-seed

# Or manually
docker-compose exec ai_services python -m alembic upgrade head
docker-compose exec postgres psql -U disaster_user -d disaster_response -f /docker-entrypoint-initdb.d/002_sample_data.sql
```

## 🌐 Access Points

Once running, access the system via:

- **Main Application**: http://localhost (via Traefik)
- **Frontend Development**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **pgAdmin (Database)**: http://localhost:5050
- **Redis Commander**: http://localhost:8081
- **Flower (Task Monitor)**: http://localhost:5555

## 👥 Default Test Accounts

Sample accounts for testing (password: `password123`):

- **Admin**: admin@disaster.response
- **First Responder**: john.responder@fire.dept  
- **Volunteer**: sarah.volunteer@rescue.org
- **Affected Individual**: mike.affected@gmail.com

## 🏗 Architecture Overview

### AI Agent Workflow

```
Request Intake → Prioritization → Task Assignment → Communication
      ↓               ↓                ↓              ↓
  AGNO Agent     AGNO Agent      AGNO Agent    AGNO Agent
  (GPT-4o-mini)  (GPT-4o-mini)   (GPT-4o-mini) (GPT-4o-mini)
```

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React SPA     │◄──►│   FastAPI       │◄──►│  PostgreSQL     │
│   Frontend      │    │   Backend       │    │  Database       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └─────────────►│     Redis       │◄─────────────┘
                        │   Cache/Queue   │
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │  AGNO Agents    │
                        │  AI Processing  │
                        └─────────────────┘
```

## 📊 Role-Based Dashboards

### Affected Individuals
- Submit emergency help requests
- Track request status and updates
- Access safety tips and resources
- Receive notifications about assistance

### Volunteers
- View available tasks and requests
- Accept and manage assigned tasks
- Update task progress and completion
- Access resource information

### First Responders
- Monitor critical and high-priority incidents
- Manage emergency dispatch operations
- Coordinate with volunteer teams
- Access real-time situation reports

### Administrators
- System-wide overview and analytics
- User and resource management
- Agent workflow monitoring
- System configuration and settings

## 🤖 AI Agent Details

### 1. Intake Agent
- **Purpose**: Process and validate incoming emergency requests
- **Model**: OpenAI GPT-4o-mini
- **Functions**: 
  - Extract key information from requests
  - Validate request completeness
  - Initial categorization

### 2. Prioritization Agent
- **Purpose**: Assess and prioritize requests based on severity
- **Model**: OpenAI GPT-4o-mini
- **Functions**:
  - Risk assessment scoring
  - Urgency classification
  - Resource requirement estimation

### 3. Assignment Agent
- **Purpose**: Match requests with appropriate responders
- **Model**: OpenAI GPT-4o-mini
- **Functions**:
  - Skill-based task assignment
  - Resource availability checking
  - Workload balancing

### 4. Communication Agent
- **Purpose**: Handle notifications and status updates
- **Model**: OpenAI GPT-4o-mini
- **Functions**:
  - Multi-channel messaging
  - Status update generation
  - Escalation handling

## 🔧 Development Commands

### Using Make (Recommended)

```bash
# Development
make dev-setup          # Set up development environment
make dev-backend        # Run backend in development mode
make dev-frontend       # Run frontend in development mode

# Docker Management
make docker-build       # Build all containers
make docker-up          # Start all services
make docker-down        # Stop all services
make docker-dev         # Start in development mode
make docker-logs        # View logs from all services
make docker-clean       # Clean up containers and volumes

# Database Operations
make db-migrate         # Run database migrations
make db-seed           # Load sample data
make db-reset          # Reset database (caution!)

# Testing and Quality
make test              # Run all tests
make test-backend      # Run backend tests only
make test-frontend     # Run frontend tests only
make lint              # Run linting
make format            # Format code

# Maintenance
make clean             # Clean temporary files
make logs              # Show application logs
```

## 🧪 Testing

### Running Tests

```bash
# All tests
make test

# Backend tests with coverage
cd ai_services
uv run pytest --cov=./ --cov-report=html

# Frontend tests
cd frontend
pnpm test
```

### Test Data

The system includes comprehensive test data:
- 5 sample users (different roles)
- 4 emergency requests (various types and priorities)
- Multiple tasks and assignments
- Resource inventory with low-stock alerts
- Notification examples

## 📝 Troubleshooting

### Common Issues

1. **Port Conflicts**:
   ```bash
   # Check which ports are in use
   netstat -tulpn | grep :<port>
   # Stop conflicting services or change ports in docker-compose.yml
   ```

2. **Database Connection Issues**:
   ```bash
   # Reset database containers
   make docker-down
   docker volume rm intelligihack-2025-final-round-challenge_postgres_data
   make docker-up
   ```

3. **OpenAI API Issues**:
   - Verify API key is correct in `.env`
   - Check API quota and billing
   - Review agent logs: `docker-compose logs ai_services`

4. **Frontend Build Issues**:
   ```bash
   # Clear node modules and reinstall
   cd frontend
   rm -rf node_modules pnpm-lock.yaml
   pnpm install
   ```

---

**Quick Start Summary:**
1. Clone repo
2. Copy `ai_services/.env.example` to `ai_services/.env`
3. Add your OpenAI API key
4. Run `make docker-up`
5. Access http://localhost
6. Login with `admin@disaster.response` / `password123`
