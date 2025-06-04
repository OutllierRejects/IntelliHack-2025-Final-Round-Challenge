# Quick Setup Guide

Get the Disaster Response Coordination System running in minutes with Docker.

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key (for AI agents)

## 🚀 Quick Start

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd IntelliHack-2025-Final-Round-Challenge
```

### 2. Environment Setup

Copy the environment template:

```bash
cp ai_services/.env.example ai_services/.env
```

Edit `ai_services/.env` with your configuration:

```env
# Required for AI Agents
OPENAI_API_KEY=your-openai-api-key-here

# Local SQLite database
DATABASE_URL=sqlite:///./disaster_response.db

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here
```

### 3. Start the System

```bash
# Start all services
make up

# Or manually with docker-compose
docker-compose up -d
```

### 4. Initialize Database

```bash
# Run database migrations and seed data
make db-setup
```

### 5. Access the Application

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **API**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📱 Test Accounts

Login with these pre-configured accounts:

=== "Affected Individual"

    ```
    Email: affected@test.com
    Password: testpass123
    ```

=== "Volunteer"

    ```
    Email: volunteer@test.com
    Password: testpass123
    ```

=== "First Responder"

    ```
    Email: responder@test.com
    Password: testpass123
    ```

=== "Administrator"

    ```
    Email: admin@test.com
    Password: testpass123
    ```

## 🔧 Development Commands

All commands available via Makefile:

```bash
# Development
make dev           # Start in development mode
make logs          # View logs
make restart       # Restart services

# Database
make db-setup      # Initialize database
make db-reset      # Reset database
make db-backup     # Backup database

# Testing
make test          # Run all tests
make test-backend  # Backend tests only
make test-frontend # Frontend tests only

# Maintenance
make down          # Stop all services
make clean         # Clean up containers and volumes
```

## 🐛 Troubleshooting

### Common Issues

!!! error "Port Already in Use"

    If ports 3000 or 8000 are in use:

    ```bash
    # Check what's using the port
    lsof -i :3000
    lsof -i :8000

    # Kill the process or change ports in docker-compose.yml
    ```

!!! error "Database Connection Failed"

    Ensure PostgreSQL is running:

    ```bash
    # Check container status
    docker-compose ps

    # View database logs
    docker-compose logs postgres
    ```

!!! error "AI Agents Not Working"

    Verify OpenAI API key:

    ```bash
    # Test API key
    curl -H "Authorization: Bearer $OPENAI_API_KEY" \
         https://api.openai.com/v1/models
    ```

### Getting Help

- Check the [Troubleshooting Guide](../troubleshooting.md)
- View application logs: `make logs`
- Check service health: `docker-compose ps`

## ✅ Next Steps

Once the system is running:

1. **[Explore User Interfaces](../user-guides/affected-individuals.md)** - Learn about role-based dashboards
2. **[Understand AI Agents](../architecture/ai-agents.md)** - How the AI workflow processes requests
3. **[API Integration](../api/authentication.md)** - Integrate with external systems
4. **[MCP Setup](../mcp/setup.md)** - Connect to LLM applications

---

Need more detailed setup? Check the [Environment Configuration](environment.md) guide.
