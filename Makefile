# Disaster Response Coordination App - Development Makefile

.PHONY: help install dev run-backend run-frontend run test lint format clean setup-db docker-up docker-down

# Default target
help:
	@echo "Disaster Response Coordination App - Development Commands"
	@echo ""
	@echo "Setup Commands:"
	@echo "  install     - Install all dependencies (backend and frontend)"
	@echo "  setup-db    - Set up database schema and sample data"
	@echo "  create-env  - Create environment file from template"
	@echo ""
	@echo "Development Commands:"
	@echo "  dev         - Run both backend and frontend in development mode"
	@echo "  run-backend - Run FastAPI backend server"
	@echo "  run-frontend- Run React frontend development server"
	@echo "  run         - Run the complete application"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker-up   - Start all services with Docker Compose"
	@echo "  docker-down - Stop all Docker services"
	@echo "  docker-build- Build all Docker images"
	@echo "  docker-dev  - Start development services only"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint        - Run linting on Python code"
	@echo "  format      - Format Python code"
	@echo "  test        - Run tests"
	@echo ""
	@echo "Utilities:"
	@echo "  clean       - Clean build artifacts and caches"
	@echo "  logs        - Show application logs"

# Installation
install:
	@echo "Installing backend dependencies with uv..."
	cd ai_services && uv sync
	@echo "Installing frontend dependencies..."
	cd frontend && pnpm install
	@echo "Installation complete!"

install-backend:
	@echo "Installing backend dependencies with uv..."
	cd ai_services && uv sync

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && pnpm install

# Database setup
setup-db:
	@echo "Setting up database schema..."
	@echo "Please run the SQL migrations in your Supabase dashboard:"
	@echo "1. ai_services/database/migrations/001_initial_schema.sql"
	@echo "2. ai_services/database/migrations/002_sample_data.sql"
	@echo ""
	@echo "Or use the Supabase CLI if available:"
	@echo "supabase db push"

# Development
dev:
	@echo "Starting development servers..."
	@make -j2 run-backend run-frontend

run-backend:
	@echo "Starting FastAPI backend server with uv..."
	cd ai_services && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	@echo "Starting React frontend development server..."
	cd frontend && pnpm dev

run:
	@echo "Starting production servers..."
	@make -j2 run-backend-prod run-frontend-prod

run-backend-prod:
	cd ai_services && uv run uvicorn main:app --host 0.0.0.0 --port 8000

run-frontend-prod:
	cd frontend && pnpm build && pnpm preview

# Agent services
run-agents:
	@echo "Starting AGNO agent services..."
	cd ai_services && uv run python -c "
import asyncio
from agno_agents.intake_agent import IntakeAgent
from agno_agents.prioritization_agent import PrioritizationAgent
from agno_agents.assignment_agent import AssignmentAgent
from agno_agents.communication_agent import CommunicationAgent

async def main():
    print('Starting agent coordination...')
    # Add agent coordination logic here
    while True:
        await asyncio.sleep(30)

asyncio.run(main())
"

# Docker Commands
docker-up:
	@echo "Starting all services with Docker Compose..."
	docker-compose up -d

docker-down:
	@echo "Stopping all Docker services..."
	docker-compose down

docker-build:
	@echo "Building all Docker images..."
	docker-compose build

docker-dev:
	@echo "Starting development services only..."
	docker-compose up -d postgres redis

docker-logs:
	@echo "Showing Docker logs..."
	docker-compose logs -f

docker-clean:
	@echo "Cleaning Docker resources..."
	docker-compose down -v
	docker system prune -f

# Code quality
lint:
	@echo "Running Python linting with uv..."
	cd ai_services && uv run ruff check .

lint-fix:
	@echo "Running Python linting with auto-fix using uv..."
	cd ai_services && uv run ruff check . --fix

format:
	@echo "Formatting Python code with uv..."
	cd ai_services && uv run ruff format .

format-check:
	@echo "Checking Python code formatting with uv..."
	cd ai_services && uv run ruff format . --check

# Testing
test:
	@echo "Running backend tests with uv..."
	cd ai_services && uv run pytest tests/ -v

test-agents:
	@echo "Testing AGNO agents with uv..."
	cd ai_services && uv run pytest tests/test_agents/ -v

test-api:
	@echo "Testing API endpoints with uv..."
	cd ai_services && uv run pytest tests/test_api/ -v

test-coverage:
	@echo "Running tests with coverage using uv..."
	cd ai_services && uv run pytest tests/ --cov=. --cov-report=html

# Utilities
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf ai_services/htmlcov/ 2>/dev/null || true
	rm -rf frontend/dist/ 2>/dev/null || true
	rm -rf frontend/node_modules/.cache/ 2>/dev/null || true
	@echo "Clean complete!"

logs:
	@echo "Application logs:"
	@if [ -f ai_services/logs/app.log ]; then \
		tail -f ai_services/logs/app.log; \
	else \
		echo "No log file found. Run the application first."; \
	fi

# Environment setup
create-env:
	@echo "Creating environment file..."
	@if [ ! -f ai_services/.env ]; then \
		cp ai_services/.env.example ai_services/.env; \
		echo "Created ai_services/.env from template"; \
		echo "Please edit ai_services/.env with your actual configuration values"; \
	else \
		echo "Environment file already exists"; \
	fi

# Docker commands (if needed)
docker-build:
	docker build -t disaster-response-app .

docker-run:
	docker run -p 8000:8000 -p 3000:3000 disaster-response-app

# Health checks
check-backend:
	@echo "Checking backend health..."
	@curl -f http://localhost:8000/health || echo "Backend not running"

check-frontend:
	@echo "Checking frontend..."
	@curl -f http://localhost:3000 || curl -f http://localhost:5173 || echo "Frontend not running"

check:
	@make check-backend
	@make check-frontend

# Database utilities
db-reset:
	@echo "This will reset the database. Are you sure? (Ctrl+C to cancel)"
	@read -p "Press Enter to continue..."
	@echo "Please reset your Supabase database and re-run the migrations"

db-backup:
	@echo "Creating database backup..."
	@echo "Please use Supabase dashboard or CLI to create a backup"

# Agent management
agent-status:
	@echo "Checking agent status..."
	@curl -f http://localhost:8000/agents/status || echo "Backend not running"

restart-agents:
	@echo "Restarting agent services..."
	@curl -X POST http://localhost:8000/agents/restart || echo "Backend not running"
