# MCP Setup and Configuration

Complete setup guide for the Model Context Protocol (MCP) integration in the Disaster Response Coordination System.

## 🚀 Quick Setup

### 1. Environment Configuration

Create or update your `.env` file with MCP-specific settings:

```env
# MCP Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001
MCP_SERVER_LOG_LEVEL=INFO

# AI Services Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database Configuration (for MCP resource providers)
DATABASE_URL=postgresql://user:password@localhost:5432/disaster_response
REDIS_URL=redis://localhost:6379/0

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### 2. Install Dependencies

```bash
# Install MCP-specific dependencies
cd ai_services
pip install -r requirements.txt

# Additional MCP dependencies
pip install mcp openai anthropic websockets
```

### 3. Start MCP Server

#### Option A: Standalone MCP Server

```bash
# Run the standalone MCP server
cd ai_services
python run_mcp_server.py
```

#### Option B: Integrated with Main API

```bash
# Start the main FastAPI server (includes MCP integration)
cd ai_services
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Verify MCP Connection

Test the MCP server is running:

```bash
# Check if MCP server is responding
curl http://localhost:8001/health

# Test MCP tools availability
curl http://localhost:8001/tools
```

## 🔧 Advanced Configuration

### MCP Server Configuration

The MCP server can be configured through environment variables or a configuration file:

```python
# ai_services/config/mcp_config.py
import os

MCP_CONFIG = {
    "server": {
        "host": os.getenv("MCP_SERVER_HOST", "localhost"),
        "port": int(os.getenv("MCP_SERVER_PORT", 8001)),
        "log_level": os.getenv("MCP_SERVER_LOG_LEVEL", "INFO"),
    },
    "tools": {
        "process_emergency_request": {
            "enabled": True,
            "timeout": 30,
            "priority": "high"
        },
        "get_agent_status": {
            "enabled": True,
            "cache_ttl": 60,
        },
        "assign_volunteer_to_task": {
            "enabled": True,
            "auto_notify": True,
        }
    },
    "resources": {
        "database_provider": {
            "connection_pool_size": 10,
            "query_timeout": 30,
        },
        "cache_provider": {
            "default_ttl": 300,
            "max_keys": 10000,
        }
    }
}
```

### Custom Tool Development

Add custom MCP tools for specific disaster response scenarios:

```python
# ai_services/mcp_integration/custom_tools.py
from mcp_integration.server import DisasterResponseMCPServer
from typing import Dict, Any

async def custom_evacuation_planner(
    location: str,
    population: int,
    threat_type: str
) -> Dict[str, Any]:
    """
    Custom tool for evacuation route planning
    """
    # Implementation for evacuation planning logic
    return {
        "evacuation_routes": [],
        "estimated_time": "30 minutes",
        "safe_zones": [],
        "transportation_needed": True
    }

# Register custom tool
mcp_server = DisasterResponseMCPServer()
mcp_server.register_tool(
    "plan_evacuation",
    custom_evacuation_planner,
    description="Plan evacuation routes for disaster response"
)
```

## 🐳 Docker Setup

### MCP Server Dockerfile

```dockerfile
# Dockerfile.mcp
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ai_services/ ./ai_services/
COPY config/ ./config/

EXPOSE 8001

CMD ["python", "ai_services/run_mcp_server.py"]
```

### Docker Compose Integration

```yaml
# docker-compose.yml (MCP service addition)
services:
  mcp-server:
    build:
      context: .
      dockerfile: Dockerfile.mcp
    ports:
      - "8001:8001"
    environment:
      - MCP_SERVER_HOST=0.0.0.0
      - MCP_SERVER_PORT=8001
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - postgres
      - redis
    networks:
      - disaster-response-network
    restart: unless-stopped
```

## 🔌 Client Integration

### Frontend MCP Integration

```typescript
// frontend/src/services/mcpService.ts
class MCPService {
  private baseURL = process.env.REACT_APP_MCP_URL || "http://localhost:8001";

  async processEmergencyRequest(requestData: any) {
    const response = await fetch(
      `${this.baseURL}/tools/process_emergency_request`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify(requestData),
      }
    );

    return response.json();
  }

  async getAgentStatus() {
    const response = await fetch(`${this.baseURL}/tools/get_agent_status`);
    return response.json();
  }

  async assignVolunteer(taskId: string, volunteerId: string) {
    return fetch(`${this.baseURL}/tools/assign_volunteer_to_task`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task_id: taskId, volunteer_id: volunteerId }),
    });
  }
}

export const mcpService = new MCPService();
```

### Python Client Example

```python
# scripts/mcp_client_example.py
import asyncio
import aiohttp
import json

class MCPClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url

    async def call_tool(self, tool_name: str, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/tools/{tool_name}",
                json=kwargs
            ) as response:
                return await response.json()

    async def process_emergency(self, description: str, location: str):
        return await self.call_tool(
            "process_emergency_request",
            description=description,
            location=location,
            priority="high"
        )

# Usage example
async def main():
    client = MCPClient()
    result = await client.process_emergency(
        "Medical emergency at downtown",
        "123 Main St, Downtown"
    )
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔍 Monitoring and Debugging

### MCP Server Logs

```bash
# View MCP server logs
tail -f ai_services/logs/mcp_server.log

# Debug mode
MCP_SERVER_LOG_LEVEL=DEBUG python ai_services/run_mcp_server.py
```

### Health Checks

```bash
# Basic health check
curl http://localhost:8001/health

# Detailed status
curl http://localhost:8001/status

# Tool availability
curl http://localhost:8001/tools
```

### Performance Monitoring

```python
# ai_services/mcp_integration/monitoring.py
import time
import logging
from functools import wraps

def monitor_tool_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logging.info(f"Tool {func.__name__} executed in {execution_time:.2f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logging.error(f"Tool {func.__name__} failed after {execution_time:.2f}s: {e}")
            raise
    return wrapper
```

## 🚨 Troubleshooting

### Common Issues

#### MCP Server Won't Start

```bash
# Check if port is already in use
netstat -tulpn | grep :8001

# Kill existing process
sudo fuser -k 8001/tcp

# Check environment variables
env | grep MCP
```

#### Database Connection Issues

```python
# Test database connectivity
from core.database import supabase

try:
    result = supabase.table("help_requests").select("count").execute()
    print("Database connection: OK")
except Exception as e:
    print(f"Database error: {e}")
```

#### Tool Registration Failures

```bash
# Verify tool registration
curl http://localhost:8001/tools | jq '.tools[].name'

# Check tool-specific logs
grep "process_emergency_request" ai_services/logs/mcp_server.log
```

### Performance Optimization

#### Caching Configuration

```python
# ai_services/mcp_integration/cache_config.py
CACHE_CONFIG = {
    "agent_status": {"ttl": 60, "max_size": 100},
    "resource_availability": {"ttl": 300, "max_size": 1000},
    "active_requests": {"ttl": 30, "max_size": 500},
}
```

#### Connection Pooling

```python
# ai_services/core/database.py
import asyncpg
from functools import lru_cache

@lru_cache(maxsize=1)
async def get_connection_pool():
    return await asyncpg.create_pool(
        dsn=DATABASE_URL,
        min_size=5,
        max_size=20,
        command_timeout=30
    )
```

## 🔄 Integration Testing

### End-to-End Test

```python
# tests/test_mcp_integration.py
import pytest
import asyncio
from mcp_integration.server import DisasterResponseMCPServer

@pytest.mark.asyncio
async def test_full_emergency_workflow():
    mcp_server = DisasterResponseMCPServer()

    # Test emergency request processing
    result = await mcp_server.process_emergency_request(
        description="Fire at 123 Main St",
        location="123 Main St",
        priority="high"
    )

    assert result["status"] == "processed"
    assert "request_id" in result

    # Test agent status
    status = await mcp_server.get_agent_status()
    assert status["active_agents"] > 0

    # Test volunteer assignment
    assignment = await mcp_server.assign_volunteer_to_task(
        task_id=result["task_id"],
        volunteer_id="test_volunteer"
    )

    assert assignment["status"] == "assigned"
```

### Load Testing

```bash
# Install load testing tool
pip install locust

# Run load test
locust -f tests/load_test_mcp.py --host=http://localhost:8001
```

## 📚 Additional Resources

- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [Tool Development Guide](tools.md)
- [Architecture Overview](overview.md)
- [API Documentation](../api/)
- [Troubleshooting Guide](../troubleshooting.md)

## 🤝 Contributing

When adding new MCP tools or modifying existing ones:

1. **Follow naming conventions**: Use descriptive, action-oriented names
2. **Add comprehensive documentation**: Include usage examples and parameter descriptions
3. **Implement error handling**: Graceful failure with informative error messages
4. **Add tests**: Unit tests and integration tests for all new tools
5. **Update documentation**: Keep this setup guide and tool reference up to date

---

For more detailed information about specific tools and their usage, see the [MCP Tools Reference](tools.md).
